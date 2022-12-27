class CarController:
    def __init__(self, dc_motor, servo=None, autonom_status=False):
        self.autonom = autonom_status
        self.dc_motor = dc_motor
        self.servo = servo

    def start(self):
        self.dc_motor.start()
        self.servo.start()  # araba çalıştığında servoda çalışsın

    def stop(self):
        self.dc_motor.stop()
        self.servo.stop()

    def pause(self):
        self.dc_motor.pause()

    def gear(self, number):
        self.dc_motor.gear(number)

    def front_drive(self):
        self.dc_motor.forward()

    def back_drive(self):
        self.dc_motor.backward()

    def left_drive(self, rotate_value):
        self.servo.rotate_left(rotate_value)

    def right_drive(self, rotate_value):
        self.servo.rotate_right(rotate_value)

    def autonom_control(self, object_status, lane_status):
        if (lane_status == " " or (object_status[1][0] == 1 and object_status[1][3] == 1)):
            self.pause()
        else:
            self.servo.servo_rotate_value(lane_status)
            self.front_drive()
        
        if (object_status[1][0] == 1 or object_status[1][1] == 1 or object_status[2] == 1):
            # print("yavaşla işik kirmizi veya sari")
            self.dc_motor.gear(1)
        else:
            self.dc_motor.gear(2)


