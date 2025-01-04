import numpy as np

from irp.tracking.track import Track

# TODO: FIX CONSTANT NEW ID'S / UPDATE DICTIONARY INSTEAD OF INITIALIZING NEW DICTIONARY EVERY FRAME:)
# TODO: FIX MAHALANOBIS DISTANCE FUNCTION (RESOLUTION SCALING) && COVARIANCE MATRIX
class ObjectTracker:
    def __init__(self, max_iou = 0.7, ttl = 3, init_frames = 3):
        self.__next_track_id = 0
        self.tracks = []

        self.max_iou = max_iou
        self.ttl = ttl
        self.init_frames = init_frames

        # self.cov = np.array([[1, 0.5], [0.5, 2]])

    def update(self, detections):
        updated_tracks = []  # Lista tracków, które zostały dopasowane do detekcji

        # self.cov = self.compute_covariance(detections, self.tracks)

        for detection in detections:
            matched = False
            for track in self.tracks:  # Iteracja przez istniejące tracki
                if self.is_match(detection, track):  # Sprawdź dopasowanie
                    track.update((detection.x, detection.y, detection.w, detection.h))  # Aktualizacja tracka
                    updated_tracks.append(track)
                    matched = True
                    print(f'matched{track.track_id}')
                    break

            if not matched:
                # Jeśli brak dopasowania, utwórz nowy track
                if not matched:
                    self.create_track(detection)
                    updated_tracks.append(self.tracks[-1])

        # Usuń tracki, które nie zostały zaktualizowane (TTL)
        self.tracks = [ track for track in self.tracks if track in updated_tracks or track.ttl > 0 ]

        return self.tracks

    def create_track(self, detection):
        new_track = Track(
            self.__next_track_id,
            (detection.x, detection.y, detection.w, detection.h)
        )
        self.tracks.append(new_track)
        self.__next_track_id += 1

    def is_match(self, detection, track):
        # Check Mahalanobis distance
        return (
            self.mahalanobis_distance(
                (detection.x + detection.w // 2, detection.y + detection.h // 2),
                (track.center_x, track.center_y)
            ) < 0.05
        )

    def predict(self):
        pass

    def init_track(self):
        pass

    def mahalanobis_distance(self, p1, p2, covariance = np.array([[1, 0.5], [0.5, 2]])):
        p1 = np.array(p1) / np.array([1920, 1080])
        p2 = np.array(p2) / np.array([1920, 1080])

        diff = p1 - p2
        inv_covariance = np.linalg.inv(covariance)
        distance = np.sqrt(np.dot(np.dot(diff, inv_covariance), diff))

        return distance

    def compute_covariance(self, detections, tracks):
        data = np.array(detections + tracks)
        return np.cov(data.T)