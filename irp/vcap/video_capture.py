from logging import currentframe

import cv2

# Class Responsible for displaying Video Player with keyboard controls
class VideoCapture:
    def __init__(self, path):
        self.path = path
        self.vcap = cv2.VideoCapture(path+"%06d.jpg")

    # public function play video
    def play_video(self):
        is_paused = False

        if not self.vcap.isOpened():
            print("Error opening video stream or file")

        while True:
            key = cv2.waitKey(1)

            if not is_paused:
                self.__open_video()

            if key == 32:  # Spacebar (ASCII Code 32) to pause video
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
    def __open_video(self):
        ret, frame = self.vcap.read()
        if ret:
            cv2.imshow('Video ' + self.path, frame)
            cv2.namedWindow('Video ' + self.path, cv2.WINDOW_NORMAL)
            # hide toolbar
            cv2.setWindowProperty('Video ' + self.path, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)