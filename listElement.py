class ListElement:
    def __init__(self, value):
        self.value = value
        self.next = None

class PathPoint(ListElement):
    def __init__(self, value):
        super().__init__(value)
        self.distance = 0