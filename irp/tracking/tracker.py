import numpy as np

from irp.tracking.track import Track

# TODO: FIX CONSTANT NEW ID'S
class ObjectTracker:
    def __init__(self, max_iou = 0.7, ttl = 60, init_frames = 3):
        self.__next_track_id = 0

        # self.metric = metric
        self.max_iou = max_iou
        self.ttl = ttl
        self.init_frames = init_frames

    def initialize_tracks(self, detections):
        tracks = []

        for detection in detections:
            tracks.append(
                Track(
                    self.__next_track_id,
                    (detection.x, detection.y, detection.w, detection.h)
                )
            )

        self.__next_track_id += 1

        return tracks

    def predict(self):
        pass

    def update(self):
        pass

    def match(self, detections, tracks):
        matches = dict()

        # TODO : FIX DETECTION MATCHING ALL DETECTIONS TO 1 TRACKER :(
        for detection in detections:
            for track in tracks:
                if self.mahalanobis_distance((detection.x + detection.w // 2, detection.y + detection.h // 2), (track.center_x, track.center_y)) < 0.5:
                    if track not in matches:
                        matches[track] = []
                    matches[track].append(detection)

        print(f'Detections: {len(detections)}')
        print(f'Matches: {len(matches)}')

        for track, detections in matches.items():
            print(f"Track ID: {track.track_id}, Associated Detections: {len(detections)}")
            for detection in detections:
                print(f"Detection: {detection.x}, {detection.y}, {detection.w}, {detection.h}")

        return matches

    def init_track(self):
        pass

    def mahalanobis_distance(self, p1, p2, covariance = np.array([[1, 0.5], [0.5, 2]])):
        p1 = np.array(p1)
        p2 = np.array(p2)

        diff = p1 - p2
        inv_covariance = np.linalg.inv(covariance)
        distance = np.sqrt(np.dot(np.dot(diff, inv_covariance), diff))

        return distance