# Deja Bounce

Minimalist, scene-based **Pong-like game with a CPU opponent**, built on top of `mini-arcade-core` and the native SDL2 backend.

Deja Bounce is **Milestone 1** of a small game that will later evolve into something weirder (time loops, horror vibes, ARG hooks). For now, it’s a clean, focused Pong implementation that doubles as a **reference game** for the `mini-arcade-core` framework.

---

## Features (Milestone 1 – Solid Pong + CPU)

- 🎮 **Playable Pong clone**
  - Two paddles, ball, walls, score.
  - Simple main menu: `Start Game` → `Quit`.
- 🧠 **CPU opponent**
  - CPU paddle tracks the ball with a max speed.
  - Difficulty controlled by paddle speed and (later) reaction/prediction tweaks.
- 🧍 vs 🤖 **Game modes**
  - Player vs CPU.
  - (Optional) CPU vs CPU “attract mode” – handy for tests / menu idle.
- ⚙️ **Configurable rules**
  - First to _N_ points wins (N is configurable).
  - Win screen with option to restart or go back to menu.
- 🧱 **Velocity-based movement**
  - No magic numbers; paddles & ball use velocities.
  - Classic Pong bounce:
    - Invert X velocity on paddle / vertical wall collision.
    - Slight variation based on impact position on the paddle.

---

## Tech Stack

- **Engine / Core:** [`mini-arcade-core`](https://github.com/your-org/mini-arcade-core)  
- **Native backend:** `mini-arcade-native-backend` (C++ / SDL2 / pybind11)  
- **Language:** Python 3.9–3.11  
- **Build:** PEP 621 `pyproject.toml` + `setuptools`  
- **CI:** GitHub Actions (lint + tests on 3.9 / 3.10 / 3.11, Slack notifications)

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/<your-org>/deja-bounce.git
cd deja-bounce
```

### 2. Create and activate a virtualenv (recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

### 3. Install dependencies

For local development (includes dev tools like pytest, black, etc.):

```bash
pip install --upgrade pip
pip install -e .[dev]
```

>Note:
>``mini-arcade-native-backend`` uses SDL2. If you are installing from source on Linux, you may need the SDL2 development package, e.g.:
>
> ```bash
> pip install --upgrade pip
> pip install -e .[dev]
> ```

If you only want to _play_ (once the project is on PyPI):

```bash
pip install deja-bounce
```

---

## Running the Game

Once installed, you can run Deja Bounce via the console script:

```bash
deja-bounce
```

Or directly via Python:

```bash
python -m deja_bounce.main
```

Depending on your local setup, there may also be a ``manage.py`` helper:


```bash
python manage.py
```