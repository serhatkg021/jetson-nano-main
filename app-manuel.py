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
servo_controller = Servo_Motor(PIN=32)
car = CarController(dc_motor=dc_controller, servo=servo_controller)


def gen_frames():  # generate frame by frame from camera
    ssd = SSD_Detection("ssd-mobilenet-v2")
    camera = cv2.VideoCapture(0)
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        frame = cv2.resize(frame, (640, 360))
        if not success:
            car.stop()
            break
        else:
            if car.autonom:
                object_status = ssd.detection(frame)
                lane_status = lane_detec(frame)
                car.autonom_control(object_status, lane_status)
                ret, buffer = cv2.imencode('.jpg', object_status[0])
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/set_status/<key>')
def set_status(key):
    if key == '0':
        car.autonom = False
    elif key == '1':
        car.autonom = True
    return ""


@app.route('/set_start/<key>')
def set_start(key):
    if key == '0':
        car.stop()
    elif key == '1':
        car.start()
    return ""


@app.route('/controller/<key>')
def controller(key):
    if key == 'ileri':
        car.front_drive()
    elif key == 'geri':
        car.back_drive()
    elif key == 'sağ':
        car.right_drive()
    elif key == 'sol':
        car.left_drive()
    elif key == 'fren':
        car.pause()
    elif key == 'vites1':
        car.gear(1)
    elif key == 'vites2':
        car.gear(2)
    elif key == 'vites3':
        car.gear(3)
    return ""


@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


@app.route('/<file>')
def jquery(file):
    return send_from_directory("./templates/", file, as_attachment=True)


if __name__ == '__main__':
    app.run(port=4040, host="0.0.0.0", debug=True)
