from bots.base import BaseBot, Move
import random

class GenerousTitForTat(BaseBot):
    """
    Cooperates first, then copies opponent's previous move.
    However, it forgives defections with a small probability.
    """

    def __init__(self, forgiveness=0.1):
        super().__init__()
        self.forgiveness = forgiveness

    def get_move(self, state):
        if not state.opponent_history:
            return Move.COOPERATE
        last_move = state.opponent_history[-1]

        # If opponent defected, maybe forgive
        if last_move == Move.DEFECT and random.random() < self.forgiveness:
            return Move.COOPERATE

        return last_move
