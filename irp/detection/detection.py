class Detection:
    def __init__(self, coordinates, class_id, confidence):
        # get coordinates
        self.x, self.y, self.w, self.h = map(int, coordinates)

        self.class_name = "person" if class_id == 0 else "unknown"
        self.colour = (255, 0, 0)
        self.confidence = confidence


    def update(self, coordinates, confidence):
        self.x, self.y, self.w, self.h = map(int, coordinates)
        self.confidence = confidence

    def __eq__(self, other):
        if not isinstance(other, Detection):
            return False
        return (self.x == other.x and
                self.y == other.y and
                self.w == other.w and
                self.h == other.h and
                self.class_name == other.class_name and
                self.confidence == other.confidence)

    def __hash__(self):
        return hash((self.x, self.y, self.w, self.h, self.class_name, self.confidence))