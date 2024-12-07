class GameLogic:
    def __init__(self):
        self.score = 0

    def add_points(self, points):
        if points > 0:
            self.score += points
        return self.score
