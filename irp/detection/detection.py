class Detection:
    def __init__(self, coordinates, class_id, confidence):
        # get coordinates
        self.x, self.y, self.w, self.h = map(int, coordinates)

        self.class_name = "person" if class_id == 0 else "unknown"
        self.colour = (255, 0, 0)
        self.confidence = confidence