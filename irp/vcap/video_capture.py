import cv2
import numpy as np

# Class Responsible for displaying Video Player with keyboard controls
class VideoManager:
    def __init__(self, path):
        self.path = path
        self.net = cv2.dnn.readNet("./yolov3.weights", "./yolov3.cfg")
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
                detections = self.__detect(frame)
                self.__open_video(frame, detections)

            key = cv2.waitKey(1)
            if key == 32:  # Space bar (ASCII Code 32) to pause video
                is_paused = not is_paused
            elif key == ord('q'):  # 'q' to quit video
                break
            elif key in (81, ord('w')):  # Left arrow or 'w' to rewind
                self.__rewind(-60)
                if is_paused:  # Jeśli wideo jest w pauzie, pokaż klatkę po przewinięciu
                    ret, frame = self.vcap.read()
                    if ret:
                        detections = self.__detect(frame)
                        self.__open_video(frame, detections)
            elif key in (83, ord('e')):  # Right arrow or 'e' to fast forward
                self.__rewind(60)
                if is_paused:  # Jeśli wideo jest w pauzie, pokaż klatkę po przewinięciu
                    ret, frame = self.vcap.read()
                    if ret:
                        detections = self.__detect(frame)
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
        for det in dets:
            cv2.rectangle(frame, (det.x, det.y), (det.w + det.x, det.h + det.y), det.colour, 2)
            cv2.putText(frame, f'{det.class_name} {det.confidence:.2f}',
                        (det.x, det.y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        cv2.imshow('Video ' + self.path, frame)
        cv2.namedWindow('Video ' + self.path, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('Video ' + self.path, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def __detect(self, frame):
        humans = []

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

class Detection:
    def __init__(self, coordinates, class_id, confidence):
        # get coordinates
        self.x, self.y, self.w, self.h = map(int, coordinates)

        self.class_name = "person" if class_id == 0 else "unknown"
        self.colour = (255, 0, 0)
        self.confidence = confidence