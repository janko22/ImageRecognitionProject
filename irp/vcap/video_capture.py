import cv2

from irp.detection.detector import ObjectDetector
from irp.tracking.tracker import ObjectTracker


# Class Responsible for displaying Video Player with keyboard controls
class VideoManager:
    def __init__(self, path):
        self.path = path
        self.detector = ObjectDetector("./yolo/yolov3.weights", "./yolo/yolov3.cfg")
        self.tracker = ObjectTracker()
        self.tracks = []
        self.matches = dict()
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
                self.tracks = self.tracker.initialize_tracks(detections)
                self.matches = self.tracker.match(detections)
                self.__open_video(frame, detections)

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
                        self.tracks = self.tracker.initialize_tracks(detections)
                        self.matches = self.tracker.match(detections)
                        self.__open_video(frame, detections)
            elif key in (83, ord('e')):
                self.__rewind(60)
                if is_paused:
                    ret, frame = self.vcap.read()
                    if ret:
                        detections = self.detector.detect_humans(frame)
                        self.tracks = self.tracker.initialize_tracks(detections)
                        self.matches = self.tracker.match(detections)
                        self.__open_video(frame, detections)

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
    def __open_video(self, frame, dets):
        # for det in dets:
        #     cv2.rectangle(frame, (det.x, det.y), (det.w + det.x, det.h + det.y), det.colour, 2)
        #     cv2.putText(frame, f'{det.class_name} {det.confidence:.2f}',
        #                 (det.x, det.y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # for track in self.tracks:
        #     cv2.circle(frame, (track.center_x, track.center_y), 4, (0, 0, 255), -1)
        #     cv2.putText(frame, f'{track.track_id}',
        #                 (track.x, track.y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # for match in self.matches:
        #     cv2.rectangle(frame, (self.matches[match].x, self.matches[match].y), (self.matches[match].w + self.matches[match].x, self.matches[match].h + self.matches[match].y), self.matches[match].colour, 2)
        #     cv2.putText(frame, f'{self.matches[match].class_name}:{match.track_id} {self.matches[match].confidence:.2f}',
        #                 (self.matches[match].x, self.matches[match].y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        #     cv2.circle(frame, (match.center_x, match.center_y), 4, (0, 255, 0), -1)

        for track, detections in self.matches.items():
            for detection in detections:
                cv2.rectangle(frame, (detection.x, detection.y), (
                detection.w + detection.x, detection.h + detection.y),
                              detection.colour, 2)
                cv2.putText(frame,
                            f'{detection.class_name}:{track.track_id} {detection.confidence:.2f}',
                            (detection.x, detection.y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 255), 1)
                cv2.circle(frame, (track.center_x, track.center_y), 4, (0, 255, 0), -1)

        cv2.imshow('Video ' + self.path, frame)
        cv2.namedWindow('Video ' + self.path, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('Video ' + self.path, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)