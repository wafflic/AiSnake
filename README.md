# 🐍 ML Snake Game

A **Python + Pygame + Q-Learning AI Snake Game** that learns to play Snake by itself, made by a high school student to practice reinforcement learning.

![ml snake.gif](https://i.ibb.co/VWrJfRXP/ml-snake.gif)

---

## 🚀 Features

👉 Classic Snake Game in **Pygame**\
👉 AI agent using **Q-Learning** that learns to play autonomously\
👉 **Persistent Q-table** using `pickle` to retain learning across sessions\
👉 **Graphical UI** with score and attempt tracking\
👉 Clean, modular object-oriented code\
👉 Resizable window with automatic border handling

---

## 🧠 How it Works

- The **AI (Q-Learning)** controls the snake:

  - State = relative position to food + danger detection + direction.
  - Action = ["up", "down", "left", "right"].
  - Reward system:
    - +10 for eating food
    - -0.5 for normal movement
    - -10 on death
  - Learns using:
    - `learning_rate = 0.1`
    - `discount_factor = 0.9`
    - `epsilon-greedy` exploration

- The **Q-table** and **Number of Attempts** are saved using `pickle` to `q_table.pkl` so the **Q-table** can keep improving over time.

---

## 🎯 Controls (Player Mode)

This project is primarily designed for **AI play**, but you can enable *player mode* by uncommenting the player loop in `main.py`:

- `Arrow Keys` or `WASD`: Move snake
- `SPACE`: Restart after death

---

## 📸 Screenshots

![screenshot1](https://i.ibb.co/277gx08b/image.png)
![screenshot2](https://i.ibb.co/gZymBqjf/image.png)
---

## 🛠 Installation

1️⃣ Clone the repository:

```bash
git clone https://github.com/yourusername/ml-snake-game.git
cd ml-snake-game
```

2️⃣ Install dependencies:

```bash
pip install pygame numpy
```

3️⃣ Place your `graphics/` folder in the project directory with:

- `apple.png`
- `head_right.png`, `head_left.png`, `head_up.png`, `head_down.png`
- `tail_right.png`, `tail_left.png`, `tail_up.png`, `tail_down.png`
- `body_horizontal.png`, `body_vertical.png`
- `Aptos.ttf` (or replace with another font)

4️⃣ Run:

```bash
python main.py
```