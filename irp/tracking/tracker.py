from irp.tracking.track import Track

class ObjectTracker:
    def __init__(self, max_iou = 0.7, ttl = 60, init_frames = 3):
        self.__next_track_id = 0
        self.tracks = []

        # self.metric = metric
        self.max_iou = max_iou
        self.ttl = ttl
        self.init_frames = init_frames

    def initialize_tracks(self, detections):
        for detection in detections:
            self.tracks.append(
                Track(
                    self.__next_track_id,
                    (detection.x, detection.y, detection.w, detection.h)
                )
            )
            self.__next_track_id += 1

        return self.tracks

    def predict(self):
        pass

    def update(self):
        pass

    def match(self):
        pass

    def init_track(self):
        pass