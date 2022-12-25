import cv2
from lane_detection import lane_detec
from ssd_mobilenet.SSD_Detection import SSD_Detection
from jetsonGPIO.DC_Motor import DC_Motor
from jetsonGPIO.Car import CarController
from flask import Flask, render_template, Response

app = Flask(__name__)

vid = cv2.VideoCapture("kayit4.mp4")
ssd = SSD_Detection("ssd-mobilenet-v2")
dc_controller = DC_Motor(ENA_PORT=33, IN1_PORT=35,
                         IN2_PORT=37, ENB_PORT=11, IN3_PORT=13, IN4_PORT=15)
car = CarController(dc_motor=dc_controller)

def gen_frames(frame):  # generate frame by frame from camera
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    car.start()
    print("Motorlar aktif")
    
    while True:
        ret, frame = vid.read()
        if not ret:
            car.stop()
            print("video tamamlandı")
            break

        frame = cv2.resize(frame, (640, 360))

        car.front_drive()
        print("ileri sürüş")

        lane_status = lane_detec(frame)
        if (lane_status == " "):
            print("Şerit yok durdu")
            car.pause()

        object_status = ssd.detection(frame)
        if (object_status[1][0] == 1 or object_status[1][1] == 1):
            print("yavaşla işik kirmizi veya sari")

        if (object_status[2] == 1):
            print("yavaşla insan var")

        if (object_status[1][0] == 1 and object_status[1][3] == 1):
            print("dur kirmizi işikta")
            car.pause()

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
