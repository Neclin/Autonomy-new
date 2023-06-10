class PathPoint():
    def __init__(self, position):
        self.position = position
        self.next = None
        self.distance = 0

    def __repr__(self):
        return f"PathPoint({str(self.position)[1:-1]}), distance: {self.distance}"