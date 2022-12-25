import cv2
from lane_detection import lane_detec
from ssd_mobilenet.SSD_Detection import SSD_Detection
from jetsonGPIO.DC_Motor import DC_Motor
from jetsonGPIO.Car import CarController

vid = cv2.VideoCapture("kayit4.mp4")
ssd = SSD_Detection("ssd-mobilenet-v2")
dc_controller = DC_Motor(ENA_PORT=33, IN1_PORT=35,
						 IN2_PORT=37, ENB_PORT=11, IN3_PORT=13, IN4_PORT=15)
car = CarController(dc_motor=dc_controller)
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
	if(lane_status == " "):
		print("Şerit yok durdu")
		car.pause()
		
	object_status = ssd.detection(frame)
	if(object_status[1][0] == 1 or object_status[1][1] == 1):
		print("yavaşla işik kirmizi veya sari")

	if(object_status[2] == 1):
		print("yavaşla insan var")
		
	if(object_status[1][0] == 1 and object_status[1][3] == 1):
		print("dur kirmizi işikta")
		car.pause()

	if cv2.waitKey(1) == ord('q'):
		break

cv2.destroyAllWindows()
