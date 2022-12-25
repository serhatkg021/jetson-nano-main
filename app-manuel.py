from flask import Flask, render_template, Response, send_from_directory
import cv2
import numpy as np
from jetsonGPIO.Car import CarController
from jetsonGPIO.DC_Motor import DC_Motor
from jetsonGPIO.Servo_Motor import Servo_Motor

from lane_detection import lane_detec
from ssd_mobilenet.SSD_Detection import SSD_Detection


app = Flask(__name__)

dc_controller = DC_Motor(ENA_PORT=33, IN1_PORT=35, IN2_PORT=37)
# servo_controller = Servo_Motor(PIN=32)
car = CarController(dc_motor=dc_controller)
car.start()

def gen_frames():  # generate frame by frame from camera
	ssd = SSD_Detection("ssd-mobilenet-v2")
	camera = cv2.VideoCapture(0)
	while True:
		# Capture frame-by-frame
		success, frame = camera.read()  # read the camera frame
		if not success:
			break
		else:
			if car.autonom:
				object_status = ssd.detection(frame)
				ret, buffer = cv2.imencode('.jpg', object_status[0])
				# ret, buffer = cv2.imencode('.jpg', frame)

			else:
				ret, buffer = cv2.imencode('.jpg', frame)
			frame = buffer.tobytes()
			yield (b'--frame\r\n'
				   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/set_status')
def set_status():
	if(car.autonom == True):
		car.autonom = False
	else:
		car.autonom = True
	return "dasdas"

@app.route('/controller/<key>')
def controller(key):
	if key == 'ileri':
		car.start()
		car.front_drive()
	elif key == 'geri':
		car.start()
		car.back_drive()
	elif key == 'sağ':
		car.stop()
	# elif key == 'sol':
	#     car.autonom = False
	return "dasdas"
	

@app.route('/video_feed')
def video_feed():
	#Video streaming route. Put this in the src attribute of an img tag
	return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
	"""Video streaming home page."""
	return render_template('index.html')


@app.route('/jquery.min.js')
def jquery():
	return send_from_directory("./templates/", "jquery.min.js", as_attachment=True)


if __name__ == '__main__':
	app.run(port=4040,host="0.0.0.0",debug=True)