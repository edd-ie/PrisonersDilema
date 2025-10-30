# 🧠 UNB Programming Club — Iterated Prisoner’s Dilemma Tournament Guide

Welcome to the UNB Programming Club’s **Iterated Prisoner’s Dilemma (IPD) Tournament** a multi-generation simulation of cooperation, competition, and algorithmic strategy.  
This guide explains the tournament’s purpose, mechanics, scoring system, and expectations for participants.

---

## 🎯 Purpose of the Tournament

The Iterated Prisoner’s Dilemma is one of the most studied problems in **game theory**, often used to explore trust, retaliation, and cooperation in uncertain environments.  
By writing autonomous “bots” to play this game, members gain experience in:

- **Algorithm design** and adaptive decision-making
- **Simulation programming** and Python automation
- **Evolutionary systems** and population dynamics
- **Analyzing strategic behavior under noise and uncertainty**

This tournament combines **competitive coding** with **research-style simulation**, allowing participants to test their strategies against others over many generations.

---

## ⚙️ Tournament Overview

Each participant writes a Python class representing a **bot** that plays the Prisoner’s Dilemma repeatedly against other bots.  
The bots earn or lose points based on how they cooperate or defect.  
Over several generations, top-performing bots “evolve,” while weaker ones are replaced — creating an evolving ecosystem of strategies.

---

### 📜 Match Structure

- Every bot plays against every other bot in **round-robin matches**.
- Each match has a fixed number of rounds (default: 200).
- In every round, both bots simultaneously choose:
  - **Cooperate (C)** → builds mutual reward
  - **Defect (D)** → betrays the opponent for short-term gain

---

### 💰 Payoff Matrix (Scoring per Round)

| Your Move | Opponent Move | Your Points | Opponent Points | Description                  |
| --------- | ------------- | ----------- | --------------- | ---------------------------- |
| **C**     | **C**         | +3          | +3              | Mutual Cooperation           |
| **C**     | **D**         | 0           | +5              | You are exploited            |
| **D**     | **C**         | +5          | 0               | You exploit opponent         |
| **D**     | **D**         | +1          | +1              | Mutual Defection (stalemate) |

> ⚖️ These numbers were chosen to ensure **defection is tempting**, but **consistent cooperation yields higher long-term rewards**.

---

### 🧩 Game Noise (Uncertainty)

To simulate real-world unpredictability:

- Each bot’s move has a small chance (`3%` by default) to **flip** —  
  meaning your bot might accidentally cooperate when it intended to defect, or vice versa.

This forces you to design **robust** strategies instead of rigid rule-followers.

---

## 🧬 Tournament Progression

The tournament proceeds across **multiple generations**:

1. **Initialization**

   - All submitted bots enter the tournament.
   - Each plays against every other bot once.

2. **Scoring**

   - Total scores are averaged per bot.
   - Cooperation rates (percentage of cooperative moves) are also recorded.

3. **Selection**

   - The top-performing bots survive to the next generation.
   - Low performers are eliminated.

4. **Visualization**

   - A live animated bar chart race shows how each bot’s score and cooperation level evolve.
   - Top bots are highlighted with glowing effects and dynamic ranks.

5. **Final Results**
   - After all generations, results are compiled.
   - The **final winner** is determined using a weighted scoring system.

---

## 🏆 Scoring System Explained

### 1. **Per-Round Points**

Bots earn points using the **payoff matrix** above.

### 2. **Per-Match Total**

Each match’s total is the sum of round points.  
The bot’s _match average_ is recorded.

### 3. **Per-Generation Score**

A bot’s _generation score_ is the mean of its match averages against all opponents.

### 4. **Overall Tournament Ranking**

To reward improvement and consistency:

- Later generations are **weighted more heavily** than earlier ones.
- Cooperation rate is used as a **tiebreaker**.

#### Weighted Formula:

\[
\text{Final Score} = \frac{\sum*{g=1}^{G} w_g \cdot \text{Score}*{g}}{\sum w_g}
\]
Where \(w_g = g\) (later generations are worth more).

If two bots tie on this value, the one with the **higher average cooperation rate** wins.

---

## 🚫 Why “Always Defect” Is Banned

While “Always Defect” is technically valid, it adds no strategic value.  
Its dominance in early generations discourages experimentation.

By banning it (and similar “mostly defect” variants), we ensure:

- Participants explore **adaptive**, **conditional**, and **creative** strategies.
- The tournament ecosystem remains **diverse** and **evolutionary**.

This rule pushes members to think about _when_ to cooperate, _when_ to retaliate, and _how_ to recover from betrayal.

---

## 🧠 What’s Expected of Participants

- Inherit from an a template class and implement the abstract function

- Your bot can:
  1. Store previous moves `(self.self_history, self.opponent_history)`
  2. Use the current round number `(state.round)`
  3. Implement memory or probabilistic logic

- Your bot must not crash — unhandled exceptions lead to disqualification.

- Follow club code of conduct — **no malicious or environment-modifying code**.

- Submit your **Python class** implementing your bot’s behavior:

---

## 📈 Visualization and Interpretation

The tournament engine generates a cinematic animation showing:

- Bot scores as evolving bars

- Dynamic rankings and highlights for the top 3 bots

- Final leaderboard with cooperation-color mapping and weighted scores

This helps participants see how their strategies adapt, survive, or fade out across generations.

---

## 🏁 Tournament Outcome

At the end of all generations:

- The bot with the highest weighted average score wins 🥇

- The most cooperative and most adaptive bots may receive honorary mentions

- Data and charts are archived for discussion and analysis

---

## 🧩 Learning Goals

By the end, participants would have explored:

- How strategies evolve in a noisy environment

- If cooperation can outperform selfishness long-term

- How to design adaptive algorithms that respond to feedback

- How simulation and visualization can reveal emergent behavior

---

🧭 Why These Concepts Were Chosen
| Concept | Purpose |
|------------|----------------|
|Iterated Prisoner’s |Dilemma Balances simplicity with rich emergent complexity.|
|Game Noise | Simulates real-world unpredictability.|
|Evolutionary Rounds | Mirrors natural selection — success through adaptation.|
|Weighted Scoring | Rewards sustained performance, not early luck.|
|Cooperation Rate Metric | Encourages designing ethical or social intelligence.|

These choices make the tournament both educational and engaging, combining competitive fun with serious algorithmic insight.

---

## 💬 Final Note

This tournament is about of algorithmic evolution.
How your bot behaves under pressure says as much about your design philosophy as your code.

Experiment, adapt, and above all — be creative.

---

# Appendix

## ⚖️ Why the Payoff for (D, D) Is Not Zero

In the **Iterated Prisoner’s Dilemma (IPD)** used in our tournament, mutual defection `(D, D)` gives both players **+1 point**, not 0.  
This design choice is deliberate and grounded in game theory.

---

## 🎯 The Classic Payoff Structure

| Your Move         | Opponent’s Move | Your Score | Opponent’s Score |
| ----------------- | --------------- | ---------- | ---------------- |
| **Cooperate (C)** | Cooperate (C)   | +3         | +3               |
| **Cooperate (C)** | Defect (D)      | +0         | +5               |
| **Defect (D)**    | Cooperate (C)   | +5         | +0               |
| **Defect (D)**    | Defect (D)      | **+1**     | **+1**           |

This follows the essential inequality that defines a true **Prisoner’s Dilemma**:

\[
T > R > P > S
\]

where  
**T** = Temptation (5), **R** = Reward (3), **P** = Punishment (1), **S** = Sucker’s payoff (0)

---

## 💡 Why Not Make (D, D) = 0?

### 1. Keeps the Game Stable

If both players received **0** for defecting, the tournament would quickly collapse into endless defection.  
There would be no gradient for improvement or recovery — every bot would perform equally badly.

### 2. Preserves Strategic Diversity

The small reward (+1) ensures that defection is **bad but not hopeless**.  
This allows more nuanced strategies to survive and recover after mutual defection.

### 3. Matches Realistic Incentives

In real-world conflicts, mutual selfishness rarely yields _nothing_.  
Both sides typically maintain minimal survival or safety — a stable but inefficient outcome.  
The +1 represents that _bare-minimum payoff_ of mutual mistrust.

### 4. Supports Evolutionary Learning

With (D, D) = 0, all strategies would converge to zero payoff, and evolutionary selection would lose meaning.  
A +1 ensures that performance differences still emerge, driving adaptation across generations.

### 5. Maintains Game-Theoretic Integrity

Changing (D, D) to 0 would break the inequality \(T > R > P > S\), turning the game into a **Deadlock Game**,  
where cooperation never pays off and defection always dominates — killing the essence of the dilemma.

---

### ✅ Summary

We use `(D, D) = +1` because it:

- Keeps the tournament balanced
- Preserves the evolutionary dynamics
- Encourages forgiveness and trust rebuilding
- Models realistic outcomes of conflict
- Maintains the mathematical properties of the Prisoner’s Dilemma

In short:

> “Defection shouldn’t end the game — it should make it harder to win.”

---

## 🏁 Final Score Calculation Explained

At the end of the evolutionary tournament, we determine each bot’s **final score** — the single value that decides its overall ranking and position on the leaderboard.

This score reflects **performance across all generations**, adjusted for **generation weighting** and **evolutionary consistency**.

---

### 🎯 Goal

We don’t just want to know which bot _won one generation_ —  
we want to know **which bot consistently performed best** over the entire evolutionary process.

The **final score** therefore combines:

1. **Average scores per generation**
2. **Weighted generation importance**
3. **Optional cooperation and stability bonuses**

---

### ⚙️ Step 1: Collect Per-Generation Data

After each generation, we record:

| Bot Name | Average Score | Cooperation Rate (%) | Generation Rank |
|----------| ------------- | -------------------- | --------------- |
| Deez     | 1523          | 45.7                 | 2               |
| Fromage  | 1644          | 53.1                 | 1               |
| Ghurt    | 1330          | 39.2                 | 3               |

This information is stored for every generation in the tournament history.

---

### ⚖️ Step 2: Apply Generation Weighting

Each generation _i_ is assigned a **weight** \( w_i \) (typically increasing with i):

\[
W = \frac{\sum*{i=1}^{n} (S_i \times w_i)}{\sum*{i=1}^{n} w_i}
\]

where

- \( S*i \) = bot’s average score in generation \_i*
- \( w_i \) = generation weight (e.g. 1 for early gens, 10 for the final gen)
- \( n \) = total number of generations

This ensures that **later generations** — where the population is more evolved and stable — **contribute more** to the final score.

Example (10 generations, linear weighting):

| Generation | Avg Score | Weight \(w_i\) | Weighted Contribution       |
| ---------- | --------- | -------------- | --------------------------- |
| 1          | 1200      | 1              | 1200                        |
| 2          | 1350      | 2              | 2700                        |
| 3          | 1450      | 3              | 4350                        |
| ...        | ...       | ...            | ...                         |
| 10         | 1700      | 10             | 17000                       |
| **Total:** | —         | 55             | **Weighted Score = 1450.9** |

So the **Final Weighted Score = 1450.9**

---

### 🧩 Step 3: Optional Cooperation Adjustment (if used)

To encourage sustainable cooperation, the final score can optionally include a **cooperation rate modifier**:

\[
FinalScore = WeightedScore \times (1 + 0.05 \times (C - 0.5))
\]

where  
\( C \) = average cooperation rate (0.0–1.0)  
This gently boosts bots that maintain healthy cooperation while penalizing pure exploiters.

Example:

- A bot with 60% cooperation gets ×1.05 boost
- A bot with 30% cooperation gets ×0.985 reduction

This keeps aggressive bots viable, but rewards those that balance aggression with collaboration.

---

### 📊 Step 4: Compute Final Leaderboard

Once all bots have their weighted final scores, we produce the leaderboard:

| Rank | Bot            | Weighted Score | Avg Coop (%) | Final Score |
| ---- | -------------- | -------------- | ------------ | ----------- |
| 🥇 1 | PavlovBot      | 1620.3         | 53.1         | **1636.5**  |
| 🥈 2 | TitForTat      | 1509.2         | 45.7         | 1512.0      |
| 🥉 3 | AdaptiveRandom | 1392.6         | 39.2         | 1385.0      |

This table is exported at the end of the simulation as both console output and (optionally) a `.csv` or `.md` file.

---

### 🧠 Step 5: Determining the Winner

The **overall winner** is the bot with the **highest final weighted score** —  
reflecting not just momentary success, but long-term adaptability, cooperation resilience, and consistent improvement across the tournament.

---

### 💡 Why This Approach Works

| Problem                 | Solution                                   |
| ----------------------- | ------------------------------------------ |
| Early lucky performance | De-emphasized by weighting                 |
| Late-generation skill   | Rewarded with higher weight                |
| Random noise            | Averaged out                               |
| Overly aggressive bots  | Balanced by optional cooperation weighting |

This produces a **fair, evolution-aware leaderboard** — where the best-designed, most resilient strategy rises to the top.

---

### ✅ In summary:

\[
FinalScore = \frac{\sum (Score_i \times Weight_i)}{\sum Weight_i} \times CooperationAdjustment
\]

or conceptually:

> **Final Score = Evolutionary Performance × Consistency × Adaptability**

That’s how we ensure the winner isn’t just the “best at one moment,”  
but the **most robust bot across the entire evolutionary timeline.**

The weighted scoring formula ensures that:

- Performance **improves meaningfully** over time.
- Bots that adapt and thrive under **increasingly intelligent competition** are rewarded.
- The final leaderboard reflects **evolutionary fitness**, not early randomness.

In short:

> “We reward evolution, not luck.”
