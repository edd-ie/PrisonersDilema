from bots.base import BaseBot, Move

class AlwaysCooperate(BaseBot):
    def get_move(self, game_state):
        return Move.COOPERATE
