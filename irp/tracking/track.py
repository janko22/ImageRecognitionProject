class Track:
    def __init__(self, track_id, coordinates):
        self.track_id = track_id

        self.x, self.y, self.w, self.h = map(int, coordinates)

        self.center_x = int(self.x + self.w / 2)
        self.center_y = int(self.y + self.h / 2)

        # self.max_iou = max_iou
        self.ttl = 0
        self.init_frames = 0

    def get_center_coordinates(self):
        return [self.center_x, self.center_y]

    def get_coordinates(self):
        return self.x, self.y, self.w, self.h

    def __eq__(self, other):
        return self.track_id == other.track_id

    def __hash__(self):
        return hash(self.track_id)