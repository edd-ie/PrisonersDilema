import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
import numpy as np


def plot_bar_race(history, all_bots, interval=800, frames_per_gen=5, show_final_leaderboard=True):
    """
    Cinematic animated bar chart race + final ranking display.
    - Bars ease toward scores
    - Scores shown above bars
    - Cooperation controls color blending
    - Fade-in/out transitions
    - Computes and prints final average-based ranking
    """
    ani = None
    generations = len(history)
    fade_frames = 8
    total_frames = fade_frames + generations * frames_per_gen + fade_frames

    # Prepare data matrices
    scores_matrix = []
    coop_matrix = []
    for gen_data in history:
        score_row, coop_row = [], []
        for bot in all_bots:
            # Only process bots that participated in this generation's history
            if bot in gen_data:
                score_row.append(gen_data[bot]["Score"])
                coop_row.append(gen_data[bot]["CoopRate"] / 100)
            else:
                score_row.append(0)
                coop_row.append(0)
        scores_matrix.append(score_row)
        coop_matrix.append(coop_row)

    # Transpose (bot-wise)
    scores_matrix = list(map(list, zip(*scores_matrix)))
    coop_matrix = list(map(list, zip(*coop_matrix)))

    # Filter out bots that scored 0 in ALL generations
    active_bot_indices = [i for i, scores in enumerate(scores_matrix) if any(scores)]

    filtered_all_bots = [all_bots[i] for i in active_bot_indices]
    filtered_scores_matrix = [scores_matrix[i] for i in active_bot_indices]
    filtered_coop_matrix = [coop_matrix[i] for i in active_bot_indices]

    # Update active bot lists and indices
    all_bots = filtered_all_bots
    scores_matrix = filtered_scores_matrix
    coop_matrix = filtered_coop_matrix

    # Colors
    base_cmap = cm.get_cmap("tab10")
    colors = [base_cmap(i % 10) for i in range(len(all_bots))]

    # Plot setup
    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor("black")

    ymax = max(max(row) for row in scores_matrix) * 1.15 if scores_matrix else 1.0
    bars = ax.bar(all_bots, [0] * len(all_bots),
                  color=[colors[i] for i in range(len(all_bots))],
                  edgecolor="white", linewidth=1.2)
    trails = ax.bar(all_bots, [0] * len(all_bots),
                    color=[(c[0], c[1], c[2], 0.15) for c in colors],
                    zorder=-1)

    ax.set_ylim(0, ymax)
    ax.set_title("Evolutionary Tournament", color="white", fontsize=18, pad=15)
    ax.set_ylabel("Score", color="white")
    ax.set_xlabel("Bots", color="white")
    ax.tick_params(colors="white")

    for spine in ax.spines.values():
        spine.set_edgecolor("white")

    labels = [ax.text(bar.get_x() + bar.get_width() / 2, 0,
                      "0", ha="center", va="bottom",
                      color="white", fontsize=10, fontweight="bold")
              for bar in bars]

    rank_labels = [ax.text(bar.get_x() + bar.get_width() / 2, ymax * 1.05,
                           "", ha="center", va="bottom",
                           color="gold", fontsize=10, fontweight="bold")
                   for bar in bars]

    # === Update function ===
    def update(frame):
        if not scores_matrix:
            return []  # No bots left

        if frame < fade_frames:  # Fade-in
            alpha = frame / fade_frames
            data_index = 0
        elif frame >= fade_frames + generations * frames_per_gen:  # Fade-out
            alpha = 1 - (frame - (fade_frames + generations * frames_per_gen)) / fade_frames
            data_index = generations - 1
        else:
            alpha = 1
            data_index = (frame - fade_frames) // frames_per_gen

        # Compute current generation ranking
        current_scores = [scores_matrix[i][min(data_index, len(scores_matrix[i]) - 1)] for i in range(len(all_bots))]
        ranked_indices = np.argsort(current_scores)[::-1]
        ranks = {idx: rank + 1 for rank, idx in enumerate(ranked_indices)}

        # Bar easing and update
        for i, bar in enumerate(bars):
            current_height = bar.get_height()
            target_height = scores_matrix[i][
                min(data_index, len(scores_matrix[i]) - 1)]  # Ensure index is not out of bounds
            eased_height = current_height + 0.15 * (target_height - current_height)
            bar.set_height(eased_height)
            trails[i].set_height(eased_height * 0.6)

            # Score label
            labels[i].set_text(f"{eased_height:.0f}")
            labels[i].set_y(eased_height + ymax * 0.01)

            # Rank label (above bar)
            rank_labels[i].set_text(f"#{ranks[i]}")
            rank_labels[i].set_y(eased_height + ymax * 0.05)

        fig.patch.set_alpha(alpha * 0.9)
        ax.set_title(f"Generation {min(data_index + 1, generations)}", color="white")
        return list(bars.patches) + labels + rank_labels + list(trails.patches)

    ani = animation.FuncAnimation(
        fig, update, frames=total_frames,
        interval=interval, blit=False, repeat=False
    )

    # === Enhanced Final Leaderboard Calculation ===
    generations_arr = np.arange(1, generations + 1)
    weights = generations_arr / generations_arr.sum()

    weighted_scores = {}
    avg_coop_rates = {}
    for i, bot in enumerate(all_bots):
        bot_scores = np.array(scores_matrix[i])
        bot_coop = np.array(coop_matrix[i])

        # IMPORTANT: Use the actual number of generations the bot *survived* for weight calculation
        num_survival_gens = len(bot_scores)
        if num_survival_gens == 0:
            weighted_avg_score = 0
            avg_coop_rate = 0
        else:
            # Use weights corresponding only to the generations the bot survived
            # This correctly applies the rule that later generations are weighted more heavily.
            survival_weights = weights[-num_survival_gens:] / weights[-num_survival_gens:].sum()

            weighted_avg_score = np.dot(bot_scores, survival_weights)
            avg_coop_rate = np.mean(bot_coop) * 100

        weighted_scores[bot] = weighted_avg_score
        avg_coop_rates[bot] = avg_coop_rate

    # Sort primarily by weighted score, secondarily by coop rate
    final_ranking = sorted(weighted_scores.items(),
                           key=lambda x: (x[1], avg_coop_rates[x[0]]),
                           reverse=True)

    print("\n🏆 FINAL OVERALL RANKING (weighted by generation, coop as tiebreaker):\n")
    print(f"{'Rank':<5} {'Bot':<25} {'Weighted Score':<18} {'Avg Coop Rate':<15}")
    print("-" * 65)
    for rank, (bot, score) in enumerate(final_ranking, 1):
        coop_rate = avg_coop_rates[bot]
        print(f"{rank:<5} {bot:<25} {score:<18.2f} {coop_rate:<15.2f}")

    return ani, final_ranking, avg_coop_rates


def draw_leaderboard(final_ranking, avg_coop_rates):
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    if not final_ranking:
        ax2.text(0.5, 0.5, "No bots to display in final ranking.", ha='center', va='center')
        ax2.set_xticks([])
        ax2.set_yticks([])
        fig2.tight_layout()
        plt.show(block=True)
        return

    bots, scores = zip(*final_ranking)
    coop_values = [avg_coop_rates[b] for b in bots]

    # Ensure color normalization handles cases where coop_values might be all zeros
    norm_max = max(coop_values) if coop_values else 1
    colors = plt.cm.viridis(np.array(coop_values) / norm_max if norm_max else 0)

    bars = ax2.bar(bots, scores, color=colors, edgecolor="black")
    ax2.set_title("Final Weighted Leaderboard (with Cooperation Influence)", fontsize=16)
    ax2.set_ylabel("Weighted Average Score")

    # Fix: explicitly set tick positions to avoid the warning
    ax2.set_xticks(np.arange(len(bots)))
    ax2.set_xticklabels(bots, rotation=30, ha="right")

    # Attach colorbar to this figure's axes explicitly
    sm = plt.cm.ScalarMappable(cmap="viridis", norm=plt.Normalize(0, norm_max))
    sm.set_array([])
    cbar = fig2.colorbar(sm, ax=ax2)
    cbar.set_label("Average Cooperation Rate (%)")

    fig2.tight_layout()
    plt.show(block=True)