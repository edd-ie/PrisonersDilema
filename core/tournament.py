from core.game_engine import GameEngine
import csv
from statistics import mean
import random

class Tournament:
    """
    Round-robin tournament with optional generation-based evolution.
    Tracks detailed stats and supports mutation/evolution over generations.
    """

    def __init__(self, bots, noise_rate=0.03):
        self.original_bots = bots  # initial population
        self.bots = list(bots)
        self.noise_rate = noise_rate
        self.engine = GameEngine(noise_rate)
        self.results = {}
        self.stats = {}

    def run(self, rounds_per_match=200):
        """Run a single round-robin tournament for current population."""
        self.results.clear()
        self.stats = {bot.__class__.__name__: {
            "total_score": 0,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "coop_rate": []
        } for bot in self.bots}

        for i, bot_a in enumerate(self.bots):
            for j, bot_b in enumerate(self.bots):
                if i >= j:
                    continue
                score_a, score_b = self.engine.play_match(bot_a, bot_b, rounds_per_match)
                name_a = bot_a.__class__.__name__
                name_b = bot_b.__class__.__name__
                self.results[(name_a, name_b)] = (score_a, score_b)

                # Update total scores
                self.stats[name_a]["total_score"] += score_a
                self.stats[name_b]["total_score"] += score_b

                # Track cooperation rate
                self.stats[name_a]["coop_rate"].append(getattr(bot_a, "last_coop_rate", 0))
                self.stats[name_b]["coop_rate"].append(getattr(bot_b, "last_coop_rate", 0))

                # Win/loss/draw
                if abs(score_a - score_b) < 1e-6:
                    self.stats[name_a]["draws"] += 1
                    self.stats[name_b]["draws"] += 1
                elif score_a > score_b:
                    self.stats[name_a]["wins"] += 1
                    self.stats[name_b]["losses"] += 1
                else:
                    self.stats[name_b]["wins"] += 1
                    self.stats[name_a]["losses"] += 1

        # Compute average cooperation rate
        for name, s in self.stats.items():
            s["coop_rate"] = mean(s["coop_rate"]) if s["coop_rate"] else 0

        return self.stats

    def leaderboard(self, sort_by="score"):
        """Return leaderboard sorted by score, wins, or cooperation rate."""
        if sort_by == "wins":
            key = lambda x: self.stats[x]["wins"]
        elif sort_by == "coop":
            key = lambda x: self.stats[x]["coop_rate"]
        else:
            key = lambda x: self.stats[x]["total_score"]

        sorted_bots = sorted(self.stats.keys(), key=key, reverse=True)
        board = []
        for name in sorted_bots:
            s = self.stats[name]
            board.append({
                "Bot": name,
                "Score": round(s["total_score"], 2),
                "Wins": s["wins"],
                "Losses": s["losses"],
                "Draws": s["draws"],
                "CoopRate": round(s["coop_rate"] * 100, 1)
            })
        return board

    def export_results(self, results_file="./data/tournament_results.csv", leaderboard_file="./data/leaderboard.csv"):
        """Export raw match results and leaderboard to CSV."""
        with open(results_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Bot A", "Bot B", "Score A", "Score B"])
            for (a, b), (score_a, score_b) in self.results.items():
                writer.writerow([a, b, score_a, score_b])

        with open(leaderboard_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Bot", "Score", "Wins", "Losses", "Draws", "Cooperation Rate (%)"])
            for row in self.leaderboard():
                writer.writerow(row.values())

    def run_evolution(self, generations=10, survival_rate=0.5, rounds_per_match=200, mutate=True):
        """
        Run generation-based evolution mode and track stats for plotting.
        Returns:
            history: list of dicts containing leaderboard stats per generation
        """
        population = [bot.__class__() for bot in self.original_bots]  # reset population
        pop_size = len(population)
        history = []  # store stats per generation

        for gen in range(generations):
            print(f"\n=== Generation {gen + 1} ===")
            self.bots = population
            self.run(rounds_per_match=rounds_per_match)
            leaderboard = self.leaderboard(sort_by="score")

            # Store snapshot for plotting
            history.append({entry["Bot"]: {"Score": entry["Score"], "CoopRate": entry["CoopRate"]}
                            for entry in leaderboard})

            # Display leaderboard
            for entry in leaderboard:
                print(f"{entry['Bot']:22s} | Score: {entry['Score']:5.0f} | Coop: {entry['CoopRate']:5.1f}%")

            # Select top performers
            survivors_count = max(1, int(pop_size * survival_rate))
            survivors = leaderboard[:survivors_count]

            # Build next generation
            new_population = []
            for entry in survivors:
                bot_class = next(b for b in population if b.__class__.__name__ == entry["Bot"]).__class__
                clones_needed = pop_size // survivors_count
                for _ in range(clones_needed):
                    clone = bot_class()
                    if mutate:
                        if hasattr(clone, "forgiveness"):
                            clone.forgiveness = max(0, min(1, clone.forgiveness + random.uniform(-0.05, 0.05)))
                    new_population.append(clone)

            population = new_population[:pop_size]

        self.bots = population
        return history
