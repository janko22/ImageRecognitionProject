import numpy as np

from irp.tracking.track import Track

class ObjectTracker:
    def __init__(self, max_iou = 0.25, ttl = 3, init_frames = 3):
        self.__next_track_id = 0
        self.tracks = []

        self.max_iou = max_iou
        self.ttl = ttl
        self.init_frames = init_frames

    def update(self, detections):
        updated_tracks = []

        for detection in detections:
            matched = False
            for track in self.tracks:
                if self.is_match(detection, track):
                    track.update((detection.x, detection.y, detection.w, detection.h))
                    updated_tracks.append(track)
                    matched = True
                    break

            if not matched:
                # If not matched create a new track
                if not matched:
                    self.create_track(detection)
                    updated_tracks.append(self.tracks[-1])

        # Delete tracks with TTL > 0
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
        # Calculate Mahalanobis distance
        mahalanobis_dist = self.mahalanobis_distance(
            (detection.x + detection.w // 2, detection.y + detection.h // 2),
            (track.center_x, track.center_y)
        )
        if mahalanobis_dist < 0.05:  # Threshold for Mahalanobis distance
            return True

        # If Mahalanobis distance fails, check IoU
        detection_bbox = (detection.x, detection.y, detection.x + detection.w, detection.y + detection.h)
        track_bbox = (track.x, track.y, track.x + track.w, track.y + track.h)

        iou = self.compute_iou(detection_bbox, track_bbox)
        if iou > self.max_iou:  # Threshold for IoU
            return True

        return False

    def predict(self):
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

    def compute_iou(self, b_box1, b_box2):
        # Unpack the coordinates of the bounding boxes
        x1, y1, x2, y2 = b_box1
        x1_2, y1_2, x2_2, y2_2 = b_box2

        # Compute the intersection rectangle
        ix1 = max(x1, x1_2)
        iy1 = max(y1, y1_2)
        ix2 = min(x2, x2_2)  # Correct: take the minimum for bottom-right corner
        iy2 = min(y2, y2_2)  # Correct: take the minimum for bottom-right corner

        # Calculate intersection area (if it exists)
        intersection_width = max(0, ix2 - ix1)
        intersection_height = max(0, iy2 - iy1)
        intersection_area = intersection_width * intersection_height

        # Calculate areas of both bounding boxes
        box1_area = (x2 - x1) * (y2 - y1)
        box2_area = (x2_2 - x1_2) * (y2_2 - y1_2)

        # Calculate union area
        union_area = box1_area + box2_area - intersection_area

        # Compute IoU
        iou = intersection_area / union_area if union_area != 0 else 0

        return iou