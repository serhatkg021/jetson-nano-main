import RPi.GPIO as GPIO
import time
class Servo_Motor:
    def __init__(self, PIN):
        self.PIN = PIN
        GPIO.setup(self.PIN, GPIO.OUT)
        self.pwm = GPIO.PWM(self.PIN, 50)

    def start(self):
        self.pwm.start(2.5)

    def rotate(self):
        self.pwm.ChangeDutyCycle(2)
        time.sleep(0.5)
        self.pwm.ChangeDutyCycle(4)
        time.sleep(0.5)
        self.pwm.ChangeDutyCycle(6)
        time.sleep(0.5)
        self.pwm.ChangeDutyCycle(4)
        time.sleep(0.5)
        self.pwm.ChangeDutyCycle(2)
        time.sleep(0.5)
        self.pwm.ChangeDutyCycle(10)
        time.sleep(0.5)
    
    def stop(self):
        self.pwm.stop()
        GPIO.cleanup()