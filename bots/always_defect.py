from bots.base import BaseBot, Move

class AlwaysDefect(BaseBot):
    def get_move(self, game_state):
        return Move.DEFECT
