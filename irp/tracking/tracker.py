from scipy.optimize import linear_sum_assignment
from irp.tracking.track import Track
import numpy as np

class ObjectTracker:
    def __init__(self, max_iou=0.25, ttl=3, init_frames=3):
        self.__next_track_id = 0
        self.tracks = []

        self.max_iou = max_iou
        self.ttl = ttl
        self.init_frames = init_frames

    def update(self, detections):
        if len(self.tracks) == 0:
            # If no tracks exist, create tracks for all detections
            for detection in detections:
                self.create_track(detection)
            return self.tracks

        # Compute cost matrix
        cost_matrix = self.compute_cost_matrix(detections)

        # Apply Hungarian Algorithm
        row_indices, col_indices = linear_sum_assignment(cost_matrix)

        # Match detections to tracks
        assigned_tracks = set()
        assigned_detections = set()

        for row, col in zip(row_indices, col_indices):
            if cost_matrix[row, col] < 1.0:  # Accept matches with reasonable cost
                track = self.tracks[col]
                detection = detections[row]
                track.update((detection.x, detection.y, detection.w, detection.h))
                assigned_tracks.add(col)
                assigned_detections.add(row)

        # Create new tracks for unmatched detections
        for i, detection in enumerate(detections):
            if i not in assigned_detections:
                self.create_track(detection)

        # Remove unmatched tracks
        self.tracks = [track for i, track in enumerate(self.tracks) if i in assigned_tracks or track.ttl > 0]

        return self.tracks

    def compute_cost_matrix(self, detections):
        # Initialize cost matrix
        num_detections = len(detections)
        num_tracks = len(self.tracks)
        cost_matrix = np.zeros((num_detections, num_tracks))

        for i, detection in enumerate(detections):
            for j, track in enumerate(self.tracks):
                mahalanobis_dist = self.mahalanobis_distance(
                    (detection.x + detection.w // 2, detection.y + detection.h // 2),
                    (track.center_x, track.center_y)
                )
                if mahalanobis_dist < 0.01:  # Favor Mahalanobis match
                    cost_matrix[i, j] = mahalanobis_dist
                else:
                    detection_bbox = (detection.x, detection.y, detection.x + detection.w, detection.y + detection.h)
                    track_bbox = (track.x, track.y, track.x + track.w, track.y + track.h)
                    iou = self.compute_iou(detection_bbox, track_bbox)
                    cost_matrix[i, j] = 1 - iou  # Use IoU as cost (1 - IoU)

        return cost_matrix

    def create_track(self, detection):
        new_track = Track(
            self.__next_track_id,
            (detection.x, detection.y, detection.w, detection.h)
        )
        self.tracks.append(new_track)
        self.__next_track_id += 1

    def mahalanobis_distance(self, p1, p2, covariance=np.array([[1, 0.5], [0.5, 2]])):
        p1 = np.array(p1) / np.array([1920, 1080])
        p2 = np.array(p2) / np.array([1920, 1080])

        diff = p1 - p2
        inv_covariance = np.linalg.inv(covariance)
        distance = np.sqrt(np.dot(np.dot(diff, inv_covariance), diff))

        return distance

    def compute_iou(self, b_box1, b_box2):
        x1, y1, x2, y2 = b_box1
        x1_2, y1_2, x2_2, y2_2 = b_box2

        ix1 = max(x1, x1_2)
        iy1 = max(y1, y1_2)
        ix2 = min(x2, x2_2)
        iy2 = min(y2, y2_2)

        intersection_width = max(0, ix2 - ix1)
        intersection_height = max(0, iy2 - iy1)
        intersection_area = intersection_width * intersection_height

        box1_area = (x2 - x1) * (y2 - y1)
        box2_area = (x2_2 - x1_2) * (y2_2 - y1_2)

        union_area = box1_area + box2_area - intersection_area
        iou = intersection_area / union_area if union_area != 0 else 0

        return iou