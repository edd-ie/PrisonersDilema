from enum import Enum

class Move(Enum):
    COOPERATE = "C"
    DEFECT = "D"

class BaseBot:
    def reset(self):
        self.self_history = []
        self.opponent_history = []

    def get_move(self, game_state):
        """Return next move. Receives GameState for context."""
        raise NotImplementedError

    def record_result(self, self_move, opponent_move):
        self.self_history.append(self_move)
        self.opponent_history.append(opponent_move)
