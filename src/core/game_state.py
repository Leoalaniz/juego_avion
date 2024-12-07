class GameState:
    def __init__(self):
        self.state = "not started"

    def start_game(self):
        self.state = "running"

    def end_game(self):
        self.state = "ended"
