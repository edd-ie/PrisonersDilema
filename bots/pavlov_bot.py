from bots.base import BaseBot, Move

class PavlovBot(BaseBot):
    """
    Win-Stay, Lose-Shift strategy:
    - Start by cooperating.
    - If last round’s payoff >= 3 (mutual cooperation or exploiting), repeat move.
    - If last round’s payoff < 3 (punished or exploited), switch move.
    """

    def __init__(self):
        super().__init__()

    def get_move(self, state):
        if not state.self_history:
            return Move.COOPERATE

        last_self = state.self_history[-1]
        last_opp = state.opponent_history[-1]

        # Compute last payoff manually
        payoff_matrix = {
            (Move.COOPERATE, Move.COOPERATE): 3,
            (Move.COOPERATE, Move.DEFECT): 0,
            (Move.DEFECT, Move.COOPERATE): 4,
            (Move.DEFECT, Move.DEFECT): 1,
        }

        payoff = payoff_matrix[(last_self, last_opp)]

        # Win-Stay-Lose-Shift rule
        if payoff >= 3:
            return last_self
        else:
            return Move.COOPERATE if last_self == Move.DEFECT else Move.DEFECT
