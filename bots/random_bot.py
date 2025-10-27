import random
from bots.base import BaseBot, Move

class RandomBot(BaseBot):
    def get_move(self, game_state):
        return random.choice([Move.COOPERATE, Move.DEFECT])
