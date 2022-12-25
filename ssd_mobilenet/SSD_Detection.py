import jetson.inference
import jetson.utils
import cv2
from traffic_light_detector import colorDetect


class SSD_Detection:
    def __init__(self, model_name):
            self.net = self.load_model(model_name)

    def load_model(self, model_name):
        try:
            return jetson.inference.detectNet(model_name)
        except:
            print("Hata: detectNet olusmadi")
            return None

    def detection(self, frame):
        img = jetson.utils.cudaFromNumpy(frame)
        detections = self.net.Detect(img)
        trafic_status = [0, 0, 0, 0]
        person_status = 0

        for obj in detections:
            class_name = self.net.GetClassDesc(obj.ClassID)
            cv2.putText(frame, "{} - {}".format(class_name, obj.Confidence),
                        (int(obj.Left), int(obj.Top)-10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

            distance_ratio = 360 / (obj.Top-obj.Bottom)
            if (class_name == "traffic light"):
                trafic_status = colorDetect(
                    frame[int(obj.Bottom):int(obj.Top), int(obj.Left):int(obj.Right)].copy())
                if distance_ratio < 5:
                    trafic_status[3] = 1
                print(trafic_status)

            if (class_name == "person"):
                if distance_ratio < 15:
                    person_status = 1
            # cv2.rectangle(frame, (int(obj.Left), int(obj.Bottom)), (int(obj.Right), int(obj.Top)), (0,0,255), 2)

        cv2.putText(frame, "FPS : {}".format(self.net.GetNetworkFPS()),
                    (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
        # cv2.imshow("OUTPUT", frame)
        return [frame, trafic_status, person_status]
