# TempleEscaping

## About

TempleEscaping is a 3D first-person escape game developed in Python using the Ursina Engine.
The player is trapped inside a temple and must solve a puzzle by activating hidden pressure plates in order to escape.

---

## Gameplay

The game starts from a main menu and places the player in a 3D environment containing:

- a temple with walls, gate, altar, torches, and decorations
- vegetation and environment objects (trees, bushes, statues)
- an escape puzzle based on pressure plates

When the player enters the temple, the gate closes and the puzzle begins.

To escape:

- find and activate **3 pressure plates**
- **2 plates activate instantly**
- **1 plate requires staying on it for a few seconds**

After activating all plates, the gate opens and the player wins.

---

## Features

* 3D first-person gameplay
* Main menu (Start / Quit)
* Escape puzzle with pressure plates
* Door open/close mechanics
* UI messages and progress counter
* Torch fire visual effect
* 3D models and textured environment

---

## Controls

* **W, A, S, D** – movement
* **Mouse** – camera control
* **ESC** – pause / exit

---

## Project Structure

---

## Installation

```bash
git clone https://github.com/mihai1702/TempleEscaping.git
cd TempleEscaping
pip install -r requirements.txt
```

---

## Run

```bash
python main.py
```