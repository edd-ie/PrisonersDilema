from bots.base import BaseBot, Move
import random

class AdaptiveRandom(BaseBot):
    """
    Chooses move probabilistically based on opponent's past behavior.
    - Tracks an opponent's cooperation ratio.
    - The more cooperative the opponent, the more likely it cooperates back.
    """

    def __init__(self):
        super().__init__()

    def get_move(self, state):
        if not state.opponent_history:
            return Move.COOPERATE

        coop_ratio = state.opponent_history.count(Move.COOPERATE) / len(state.opponent_history)
        # Add randomness so it can't be easily exploited
        prob_coop = 0.3 + 0.7 * coop_ratio

        return Move.COOPERATE if random.random() < prob_coop else Move.DEFECT
