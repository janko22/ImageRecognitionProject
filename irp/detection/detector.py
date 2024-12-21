import cv2
import numpy as np

from irp.detection.detection import Detection

class ObjectDetector:
    def __init__(self, weights, cfg):
        self.net = cv2.dnn.readNet(weights, cfg)
        # self.humans = [] # ERROR DETECTIONS ARE NOT DELETED EACH FRAME

    def detect_humans(self, frame):
        humans = [] # IT WORKED THO

        (height, width) = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)

        output_layer_name = self.net.getUnconnectedOutLayersNames()
        output_layers = self.net.forward(output_layer_name)

        for output in output_layers:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if class_id == 0 and confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)

                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w /2)
                    y = int(center_y - h /2)

                    humans.append(Detection([x, y, w, h], class_id, confidence))

        return humans