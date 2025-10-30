from core.game_engine import GameEngine
import csv
from statistics import mean
import random
from bots.base import Move  # Assuming Move class is used for winner determination


class Tournament:
    """
    Round-robin tournament with generation-based evolution.
    Tracks detailed stats and supports comprehensive historical export.
    """

    def __init__(self, bots, noise_rate=0.03):
        self.original_bots = bots  # initial population
        self.bots = list(bots)
        self.noise_rate = noise_rate
        self.engine = GameEngine(noise_rate)

        # self.results is temporary per run, self.stats is per run
        self.stats = {}
        self.bot_class_map = {bot.__class__.__name__: bot.__class__ for bot in self.original_bots}

        # NEW: History lists for comprehensive export
        self.leaderboard_history = []
        self.match_history = []

    def run(self, rounds_per_match=200, generation=1):
        """Run a single round-robin tournament for current population, recording match outcomes."""
        self.results = {}
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

                # Determine match winner for historical tracking
                winner = "Draw"
                if abs(score_a - score_b) > 1e-6:
                    winner = name_a if score_a > score_b else name_b

                # Populate self.results (for run_evolution to use)
                self.results[(name_a, name_b)] = (score_a, score_b)

                # NEW: Populate match history
                self.match_history.append({
                    "Generation": generation,
                    "Bot A": name_a,
                    "Bot B": name_b,
                    "Score A": score_a,
                    "Score B": score_b,
                    "Winner": winner
                })

                # Update total scores
                self.stats[name_a]["total_score"] += score_a
                self.stats[name_b]["total_score"] += score_b

                # Track cooperation rate
                self.stats[name_a]["coop_rate"].append(getattr(bot_a, "last_coop_rate", 0))
                self.stats[name_b]["coop_rate"].append(getattr(bot_b, "last_coop_rate", 0))

                # Win/loss/draw
                if winner == "Draw":
                    self.stats[name_a]["draws"] += 1
                    self.stats[name_b]["draws"] += 1
                elif winner == name_a:
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

    def export_match_history(self, results_file="./data/tournament_results.csv"):
        """Export raw match results and winner/loser per generation to CSV."""
        if not self.match_history:
            print("No match history to export.")
            return

        with open(results_file, "w", newline="") as f:
            fieldnames = ["Generation", "Bot A", "Bot B", "Score A", "Score B", "Winner"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.match_history)

    def export_leaderboard_history(self, leaderboard_history_file="./data/leaderboard_history.csv"):
        """Export full leaderboard rankings per generation to CSV."""
        if not self.leaderboard_history:
            print("No leaderboard history to export.")
            return

        fieldnames = ["Generation", "Rank", "Bot", "Score", "Wins", "Losses", "Draws", "Cooperation Rate (%)"]

        with open(leaderboard_history_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.leaderboard_history)

    def export_results(self, results_file="./data/tournament_results.csv",
                       leaderboard_history_file="./data/leaderboard_history.csv"):
        """Wrapper to export all tournament data."""
        self.export_match_history(results_file)
        self.export_leaderboard_history(leaderboard_history_file)

    def run_evolution(self, generations=10, survival_rate=0.5, rounds_per_match=200, mutate=True):
        """
        Run generation-based evolution mode and track stats for plotting and export.
        """
        bot_names = list(self.bot_class_map.keys())
        population = [self.bot_class_map[name]() for name in bot_names]
        pop_size = len(population)
        history = []

        # Reset history lists on new run
        self.leaderboard_history = []
        self.match_history = []

        allowed_bot_names = set(bot_names)

        for gen in range(generations):
            current_gen = gen + 1
            print(f"\n=== Generation {current_gen} ===")

            self.bots = [bot for bot in population if bot.__class__.__name__ in allowed_bot_names]

            self.run(rounds_per_match=rounds_per_match, generation=current_gen)

            leaderboard_full = self.leaderboard(sort_by="score")
            leaderboard = [entry for entry in leaderboard_full if entry["Bot"] in allowed_bot_names]

            # RULE ENFORCEMENT: Banned Strategy Check (only needed after first generation run)
            if gen == 0:
                banned_bots = set()
                # Check for >90% defection (Cooperation Rate < 10.0%)
                for entry in leaderboard:
                    if entry["CoopRate"] < 10.0:
                        banned_bots.add(entry["Bot"])
                        print(
                            f"[RULE VIOLATION] {entry['Bot']} banned: Coop Rate ({entry['CoopRate']:.1f}%) < 10.0% (>90% Defect).")

                if banned_bots:
                    allowed_bot_names -= banned_bots
                    # Rebuild leaderboard, excluding banned bots
                    leaderboard = [entry for entry in leaderboard if entry["Bot"] not in banned_bots]

            # --- Leaderboard History Export Preparation ---
            for rank, entry in enumerate(leaderboard, 1):
                self.leaderboard_history.append({
                    "Generation": current_gen,
                    "Rank": rank,
                    "Bot": entry["Bot"],
                    "Score": entry["Score"],
                    "Wins": entry["Wins"],
                    "Losses": entry["Losses"],
                    "Draws": entry["Draws"],
                    "Cooperation Rate (%)": entry["CoopRate"]
                })
            # ---------------------------------------------

            # --- Termination Check ---
            if len(leaderboard) <= 1:
                if leaderboard:
                    print(
                        f"\n[TOURNAMENT TERMINATED] Only one unique strategy ({leaderboard[0]['Bot']}) remains. Stopping evolution.")
                    history.append({entry["Bot"]: {"Score": entry["Score"], "CoopRate": entry["CoopRate"]}
                                    for entry in leaderboard})
                else:
                    print("\n[TOURNAMENT TERMINATED] No unique strategies remain. Stopping evolution.")
                break
            # --------------------------

            # Store snapshot for plotting
            history.append({entry["Bot"]: {"Score": entry["Score"], "CoopRate": entry["CoopRate"]}
                            for entry in leaderboard})

            # Display leaderboard
            for entry in leaderboard:
                print(f"{entry['Bot']:22s} | Score: {entry['Score']:5.0f} | Coop: {entry['CoopRate']:5.1f}%")

            # Selection and Cloning Logic
            pop_size_current = len(allowed_bot_names)
            survivors_count = max(1, int(len(leaderboard) * survival_rate))
            survivors = leaderboard[:survivors_count]

            # Build next generation
            new_population = []
            for entry in survivors:
                bot_class = self.bot_class_map[entry["Bot"]]
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