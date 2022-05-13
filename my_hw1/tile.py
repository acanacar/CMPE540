class Tiles:
    def __init__(self):
        self.matrix = [[None, None, None],
                       [None, "c", None],
                       [None, None, None]]

    @property
    def center(self):
        return self.matrix[1][1]

    @property
    def left(self):
        return self.matrix[1][0]

    @property
    def right(self):
        return self.matrix[1][2]

    @property
    def down(self):
        return self.matrix[2][1]
    @property
    def up(self):
        return self.matrix[0][1]


