import cv2

class CarController:
    def __init__(self, dc_motor, servo=None, autonom_status=False):
        # self.camera = cv2.VideoCapture(0)
        self.autonom = autonom_status
        self.dc_motor = dc_motor
        self.servo = servo

    def start(self):
        self.dc_motor.start()

    def pause(self):
        self.dc_motor.pause()

    def front_drive(self):
        self.dc_motor.forward()
        # self.servo.start()

        # self.servo.rotate()

    def back_drive(self):
        self.dc_motor.backward()

    def left_drive(self):
        self.pause()
        # servo turn left

    def right_drive(self):
        self.pause()
        # servo turn right

    def stop(self):
        self.dc_motor.stop()
