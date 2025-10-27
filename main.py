from core.tournament import Tournament
from bots.tit_for_tat import TitForTat
from bots.random_bot import RandomBot
from bots.always_cooperate import AlwaysCooperate
from bots.always_defect import AlwaysDefect
from bots.generous_tit_for_tat import GenerousTitForTat
from bots.pavlov_bot import PavlovBot
from bots.adaptive_random import AdaptiveRandom
from core.util import plot_bar_race
import matplotlib.pyplot as plt

def main():
    bots = [
        TitForTat(),
        GenerousTitForTat(),
        PavlovBot(),
        AdaptiveRandom(),
        RandomBot(),
        AlwaysCooperate(),
        AlwaysDefect()
    ]

    tournament = Tournament(bots, noise_rate=0.03)

    history = tournament.run_evolution(
        generations=10,
        survival_rate=0.70,
        rounds_per_match=500,
        mutate=True
    )

    # Export final results
    tournament.export_results()

    # Plot evolution
    all_bots = [
        "TitForTat",
        "GenerousTitForTat",
        "PavlovBot",
        "AdaptiveRandom",
        "RandomBot",
        "AlwaysCooperate",
        "AlwaysDefect"
    ]

    ani = plot_bar_race(history, all_bots, interval=1200, frames_per_gen=6)

    try:
        ani.save("tournament_evolution.mp4", writer="ffmpeg", fps=5)
        print("[Info] Video saved as 'tournament_evolution.mp4'.")
    except Exception as e:
        print(f"[Warning] Could not save video: {e}")
    plt.show()


if __name__ == "__main__":
    main()
