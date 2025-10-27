import matplotlib
matplotlib.use("TkAgg")  # Ensure PyCharm works
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm

def plot_bar_race(history, all_bots, interval=800, frames_per_gen=5):
    """
    Slow, cinematic animated bar chart race for evolutionary tournament:
    - Bars ease toward score
    - Score trails behind
    - Cooperation-based color intensity
    - Fade-in/fade-out
    - Frames repeated per generation for smooth slow motion
    """
    generations = len(history)
    fade_frames = 8
    total_frames = fade_frames + generations * frames_per_gen + fade_frames

    # Prepare data matrices
    scores_matrix = []
    coop_matrix = []
    for gen_data in history:
        score_row, coop_row = [], []
        for bot in all_bots:
            if bot in gen_data:
                score_row.append(gen_data[bot]["Score"])
                coop_row.append(gen_data[bot]["CoopRate"] / 100)
            else:
                score_row.append(0)
                coop_row.append(0)
        scores_matrix.append(score_row)
        coop_matrix.append(coop_row)

    # Transpose (per bot)
    scores_matrix = list(map(list, zip(*scores_matrix)))
    coop_matrix = list(map(list, zip(*coop_matrix)))

    # Colors
    base_cmap = cm.get_cmap("tab10")
    colors = [base_cmap(i % 10) for i in range(len(all_bots))]

    # Plot setup
    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor("black")

    ymax = max(max(row) for row in scores_matrix) * 1.15
    bars = ax.bar(all_bots, [0]*len(all_bots),
                  color=[colors[i] for i in range(len(all_bots))],
                  edgecolor="white", linewidth=1.2)
    trails = ax.bar(all_bots, [0]*len(all_bots),
                    color=[(c[0], c[1], c[2], 0.15) for c in colors],
                    zorder=-1)

    ax.set_ylim(0, ymax)
    ax.set_title("Evolutionary Tournament", color="white", fontsize=18, pad=15)
    ax.set_ylabel("Score", color="white")
    ax.set_xlabel("Bots", color="white")
    ax.tick_params(colors="white")

    for spine in ax.spines.values():
        spine.set_edgecolor("white")

    labels = [ax.text(bar.get_x() + bar.get_width()/2, 0,
                      "0", ha="center", va="bottom",
                      color="white", fontsize=10, fontweight="bold")
              for bar in bars]

    # === Update function ===
    def update(frame):
        # Fade-in/out handling
        if frame < fade_frames:  # Fade-in
            alpha = frame / fade_frames
            data_index = 0
        elif frame >= fade_frames + generations * frames_per_gen:  # Fade-out
            alpha = 1 - (frame - (fade_frames + generations * frames_per_gen)) / fade_frames
            data_index = generations - 1
        else:
            alpha = 1
            data_index = (frame - fade_frames) // frames_per_gen

        # Bar easing and update
        for i, bar in enumerate(bars):
            current_height = bar.get_height()
            target_height = scores_matrix[i][data_index]
            eased_height = current_height + 0.15 * (target_height - current_height)
            bar.set_height(eased_height)

            trails[i].set_height(eased_height * 0.6)

            # Update label
            labels[i].set_text(f"{eased_height:.0f}")
            labels[i].set_y(eased_height + ymax*0.01)

            # Color blending by cooperation
            coop = coop_matrix[i][data_index]
            base_color = colors[i][:3]
            blended_color = tuple([c * (0.5 + 0.5*coop) for c in base_color])
            bar.set_color(blended_color + (alpha,))

        # Background fade
        fig.patch.set_alpha(alpha * 0.9)

        # Update title
        ax.set_title(f"Generation {min(data_index + 1, generations)}", color="white")

        return list(bars.patches) + labels + list(trails.patches)

    ani = animation.FuncAnimation(
        fig, update, frames=total_frames,
        interval=interval, blit=False, repeat=False
    )

    return ani
