import cv2

class CarController:
	def __init__(self, dc_motor, servo=None, autonom_status=False, camera_index=0):
		self.autonom = autonom_status
		self.dc_motor = dc_motor
		self.servo = servo
		self.camera_index = camera_index

	def cam_start(self):
		self.camera = cv2.VideoCapture(self.camera_index)
	
	def cam_stop(self):
		self.camera.release()

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

	def left_drive(self):
		self.servo.rotate_left()

	def right_drive(self):
		self.servo.rotate_right()

	# def autonom_control(self, object_status):
	def autonom_control(self, object_status, lane_status):
		try:
			# if (object_status[1][0] == 1 and object_status[1][3] == 1):
			if (lane_status == " " or object_status[1][0] == 1 or object_status[2] == 1):
				print("YOL - TRAFIK KIRMIZI")
				self.pause()
			else:
				print("YOL MUSAIT")
				self.servo.servo_rotate_value(lane_status)
				self.front_drive()

			if (object_status[1][0] == 1 or object_status[1][1] == 1):
				print("yavaşla işik kirmizi veya sari")
				self.dc_motor.gear(0.5)
			else:
				self.dc_motor.gear(1)
		except:
			print("otonom hata")


