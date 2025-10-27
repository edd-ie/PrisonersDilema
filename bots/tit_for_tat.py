from bots.base import BaseBot, Move

class TitForTat(BaseBot):
    def get_move(self, game_state):
        if not game_state.opponent_history:
            return Move.COOPERATE
        return game_state.last_opponent_move()
