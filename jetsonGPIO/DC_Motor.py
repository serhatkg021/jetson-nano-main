import RPi.GPIO as GPIO


class DC_Motor:
    def __init__(self, ENA_PORT, IN1_PORT, IN2_PORT):
        self.ENA = ENA_PORT
        self.IN1 = IN1_PORT
        self.IN2 = IN2_PORT
        self.speed = 0

    def start(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN2, GPIO.OUT, initial=GPIO.LOW)
        self.pwm = GPIO.PWM(self.ENA, 50)
        self.pwm.start(self.speed)

    def forward(self):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)

    def backward(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)

    def pause(self):
        self.speed = 0
        self.pwm.ChangeDutyCycle(self.speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)

    def gear(self, number):
        self.speed = number * 33
        self.pwm.ChangeDutyCycle(self.speed)

    def stop(self):
        self.speed = 0
        self.pwm.ChangeDutyCycle(self.speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.cleanup()
