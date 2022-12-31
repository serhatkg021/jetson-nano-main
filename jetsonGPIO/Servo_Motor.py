import RPi.GPIO as GPIO
import global_variables


class Servo_Motor:
    def __init__(self, PIN):
        self.PIN = PIN
        GPIO.setup(self.PIN, GPIO.OUT)
        self.pwm = GPIO.PWM(self.PIN, 50)

    def start(self):
        self.pwm.start(2.5)
        self.default_rotate()

    def stop(self):
        self.default_rotate()
        self.pwm.stop()

    # başlangıçta düz gitmesi için gereken servo açısının ayarlanması
    def default_rotate(self):
        self.pwm.ChangeDutyCycle(global_variables.DEFAULT_SERVO_ANGLE_VALUE)

    def rotate_left(self):  # sola dönüş
        self.pwm.ChangeDutyCycle(global_variables.LEFT_SERVO_ANGLE_VALUE)

    def rotate_right(self):  # sağa dönüş
        self.pwm.ChangeDutyCycle(global_variables.RIGHT_SERVO_ANGLE_VALUE)

    def servo_rotate_value(self, rotate_value):
        # gelen dönme değeri, -1 ile +1 arasında ki değere e göre sola veya sağa dönüş miktarı hesaplacanak
        leftorright_rotate_value = (rotate_value * 6.25) * 0.4
        leftorright_rotate_value = global_variables.DEFAULT_SERVO_ANGLE_VALUE - leftorright_rotate_value            
        self.pwm.ChangeDutyCycle(leftorright_rotate_value)