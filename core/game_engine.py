import random
from core.game_state import GameState
from bots.base import Move

class GameEngine:
    """
    GameEngine handles the logic for iterated Prisoner's Dilemma matches
    between two bots. Includes tunable payoff matrix and stochastic noise
    to simulate miscommunication or execution errors.
    """

    def __init__(self, noise_rate=0.03, T=4, R=3, P=1, S=0):
        """
        Parameters
        ----------
        noise_rate : float
            Probability that a bot's move will be flipped (simulate noise).
        T, R, P, S : float
            Temptation, Reward, Punishment, and Sucker payoffs respectively.
        """
        self.noise_rate = noise_rate

        # Balanced payoff matrix (less extreme than default)
        self.PAYOFFS = {
            (Move.COOPERATE, Move.COOPERATE): (R, R),
            (Move.COOPERATE, Move.DEFECT):    (S, T),
            (Move.DEFECT, Move.COOPERATE):    (T, S),
            (Move.DEFECT, Move.DEFECT):       (P, P),
        }

    def maybe_flip(self, move):
        """Simulate execution error with probability `noise_rate`."""
        if random.random() < self.noise_rate:
            return Move.COOPERATE if move == Move.DEFECT else Move.DEFECT
        return move

    def play_match(self, bot_a, bot_b, rounds=200):
        """
        Play an iterated Prisoner's Dilemma match between two bots.

        Returns
        -------
        (float, float) : total scores for bot_a and bot_b.
        """

        score_a = score_b = 0
        bot_a.reset()
        bot_b.reset()

        # Optional tracking for analytics (cooperation ratio)
        coop_count_a = coop_count_b = 0

        for r in range(rounds):
            state_a = GameState(bot_a.self_history, bot_a.opponent_history, r)
            state_b = GameState(bot_b.self_history, bot_b.opponent_history, r)

            move_a = self.maybe_flip(bot_a.get_move(state_a))
            move_b = self.maybe_flip(bot_b.get_move(state_b))

            payoff_a, payoff_b = self.PAYOFFS[(move_a, move_b)]
            score_a += payoff_a
            score_b += payoff_b

            if move_a == Move.COOPERATE:
                coop_count_a += 1
            if move_b == Move.COOPERATE:
                coop_count_b += 1

            bot_a.record_result(move_a, move_b)
            bot_b.record_result(move_b, move_a)

        # Store stats for analysis
        bot_a.last_coop_rate = coop_count_a / rounds
        bot_b.last_coop_rate = coop_count_b / rounds

        return score_a, score_b
