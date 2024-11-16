import cv2
from ultralytics import YOLO
import numpy as np

# Class Responsible for displaying Video Player with keyboard controls
class VideoManager:
    def __init__(self, path):
        self.path = path
        self.yolo = YOLO('yolov8s.pt')
        #self.net = cv2.dnn.readNetFromTorch('yolov8s.pt')
        self.vcap = cv2.VideoCapture(path+"%06d.jpg")

    # public function play video and handle the controls
    def play_video(self):
        is_paused = False

        if not self.vcap.isOpened():
            print("Error opening video stream or file")

        while True:
            ret, frame = self.vcap.read()
            key = cv2.waitKey(1)

            if not is_paused:
                self.__open_video(self.__detect(frame))

            if key == 32:  # Space bar (ASCII Code 32) to pause video
                is_paused = not is_paused
            elif key == ord('q'):  # q quit video
                break
            elif key == 81:  # left arrow to move to past frames
                self.__rewind(-60)
            elif key == ord('w'):  # w to move to past frames
                self.__rewind(-60)
            elif key == 83:  # right arrow to move to future frames
                self.__rewind(60)
            elif key == ord('e'):  # e to move to future frames
                self.__rewind(60)

        self.vcap.release()
        cv2.destroyAllWindows()

    # function to rewind video by frame count
    def __rewind(self, frame_count):
        current_frame = self.vcap.get(cv2.CAP_PROP_POS_FRAMES)
        next_frame = max(0, current_frame + frame_count)
        self.vcap.set(cv2.CAP_PROP_POS_FRAMES, next_frame)
        self.__open_video()

    def __get_video_info(self):
        pass

    # function to open video window
    def __open_video(self, dets):
        ret, frame = self.vcap.read()
        if ret:
            for det in dets:
                cv2.rectangle(frame, (det.x1, det.y1), (det.x2, det.y2), det.colour, 2)

            cv2.imshow('Video ' + self.path, frame)
            cv2.namedWindow('Video ' + self.path, cv2.WINDOW_NORMAL)
            # hide toolbar
            cv2.setWindowProperty('Video ' + self.path, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def __detect(self, frame):
        self.results = self.yolo.track(frame, stream=True, classes=[0])
        dets = []

        for result in self.results:
            classes_names = result.names

            # iterate over each bounding box in results
            for box in result.boxes:
                # check if confidence is greater than 40 percent
                if box.conf[0] > 0.4:
                    dets.append(Detection(result, box))

        return dets

class Detection:
    def __init__(self, result, box):
        # get coordinates
        [x1, y1, x2, y2] = box.xyxy[0]
        # convert to int
        self.x1, self.y1, self.x2, self.y2 = int(x1), int(y1), int(x2), int(y2)

        # get the class
        self.cls = int(box.cls[0])

        # get the class name
        classes_names = result.names
        self.class_name = classes_names[self.cls]

        self.colour = (255, 0, 0)