class GameState:
    def __init__(self, self_history, opponent_history, round_number):
        self.self_history = list(self_history)
        self.opponent_history = list(opponent_history)
        self.round_number = round_number

    def last_opponent_move(self):
        return self.opponent_history[-1] if self.opponent_history else None
