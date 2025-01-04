import cv2

from irp.detection.detector import ObjectDetector
from irp.tracking.tracker import ObjectTracker


# Class Responsible for displaying Video Player with keyboard controls
class VideoManager:
    def __init__(self, path):
        self.path = path
        self.detector = ObjectDetector("./yolo/yolov3.weights", "./yolo/yolov3.cfg")
        self.tracker = ObjectTracker()
        self.vcap = cv2.VideoCapture(path+"%06d.jpg")

    # public function play video and handle the controls
    def play_video(self):
        is_paused = False

        if not self.vcap.isOpened():
            print("Error opening video stream or file")
            return

        while True:
            if not is_paused:
                ret, frame = self.vcap.read()
                if not ret:
                    is_paused = True
                    continue
                detections = self.detector.detect_humans(frame)
                tracks = self.tracker.update(detections)
                self.__open_video(frame, tracks)

            # controls
            key = cv2.waitKey(1)
            if key == 32:
                is_paused = not is_paused
            elif key == ord('q'):
                break
            elif key in (81, ord('w')):
                self.__rewind(-60)
                if is_paused:
                    ret, frame = self.vcap.read()
                    if ret:
                        detections = self.detector.detect_humans(frame)
                        tracks = self.tracker.update(detections)
                        self.__open_video(frame, tracks)
            elif key in (83, ord('e')):
                self.__rewind(60)
                if is_paused:
                    ret, frame = self.vcap.read()
                    if ret:
                        detections = self.detector.detect_humans(frame)
                        tracks = self.tracker.update(detections)
                        self.__open_video(frame, tracks)

        self.vcap.release()
        cv2.destroyAllWindows()

    # function to rewind video by frame count
    def __rewind(self, frame_count):
        current_frame = self.vcap.get(cv2.CAP_PROP_POS_FRAMES)
        next_frame = max(0, current_frame + frame_count)
        self.vcap.set(cv2.CAP_PROP_POS_FRAMES, next_frame)

    def __get_video_info(self):
        pass

    # function to open video window
    def __open_video(self, frame, matches):

        for match in matches:
            cv2.rectangle(frame,(match.x, match.y),(match.x + match.w, match.y + match.h), (255, 0, 0),2)
            cv2.putText(frame,f'ID:{match.track_id}',(match.x, match.y - 10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0, 0, 255),1)
            cv2.circle(frame,(match.center_x, match.center_y),4,(0, 255, 0),-1)

            # height, width, channels = frame.shape
            # print(f'Szerokość: {width}, Wysokość: {height}, Kanały: {channels}')

        cv2.imshow('Video ' + self.path, frame)
        cv2.namedWindow('Video ' + self.path, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('Video ' + self.path, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)