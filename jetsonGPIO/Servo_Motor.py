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

    def servo_rotate_value(rotate_value):
        # gelen dönme değeri, -1 ile +1 arasında ki değere e göre sola veya sağa dönüş miktarı hesaplacanak
        leftorright_rotate_value = 0
        if -1 <= rotate_value < 0:
            # servo 90 derece düz ise derece artarken sola azalırken sağa gidiyor diye düşünerek yapıyorum bu değişibilir
            # 15 180 derece 7.5 90 derece dersek her 2.5 30 dereceye denk gelir yani 30 sola 30 sağa şeklinde yapıyorum.
            leftorright_rotate_value = 10

        elif 0 < rotate_value >= 1:
            leftorright_rotate_value == 5

        else:
            leftorright_rotate_value = 7.5

        return rotate_value
