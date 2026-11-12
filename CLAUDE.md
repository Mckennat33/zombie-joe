# Zombie Joe

## Working mode (overrides my global CLAUDE.md)

This project is NOT a learning project. Ignore the "Learning Mode" rules in my global `~/.claude/CLAUDE.md` while working here:

- Write and edit code directly. No need to ask first or give hints instead of code.
- Don't suggest Anki cards or quiz me unless I ask.
- Still keep code simple and readable, and briefly call out anything non-obvious or anything I should double-check.
- Commit or push only when I ask.

## The game

A 2D top-down zombie shooter in Python. Joe moves around his town killing zombies.

- Levels made of waves; zombies get harder each level.
- Map areas unlock as you progress.
- Guns unlock as you progress.
- 1 or 2 players (local co-op first, shared screen). Online play may come later.

## Tech stack

- Python 3, `pygame-ce` (imported as `pygame`), `pytmx` for loading Tiled maps
- Maps are made in Tiled and saved as `.tmx` in `maps/`
- Dependencies in `requirements.txt`; use a venv at `.venv/`

## Project layout

- `main.py`: entry point, creates `Game` and runs it
- `game/`: all game code, one main class per file (`player.py`, `zombie.py`, `weapon.py`, `level.py`, `camera.py`, `hud.py`, `controls.py`, `save.py`, `settings.py`, `game.py`)
- `data/`: JSON stats (weapons, zombies, levels, controls)
- `maps/`: Tiled `.tmx` maps and `.tsx` tilesets
- `assets/`: images, sounds, fonts
- `saves/`: runtime save files (gitignored)

## Conventions

- **Support multiple players everywhere.** Keep players in a list and never assume there's a single player. Zombies target the nearest player; the camera and HUD handle 1–2 players.
- **`Player` never reads the keyboard directly.** `controls.py` turns input into actions per player and passes them to `Player`, so input can later come from a controller or the network.
- **Gameplay numbers live in `data/*.json`**, not in code (damage, fire rate, zombie speed/health, wave sizes, unlock levels).
- **Constants live in `game/settings.py`** (screen size, FPS, tile size, colors).
- Use frame-rate-independent movement (multiply by delta time).
- Build features incrementally and keep the game runnable after each change.

## Running

```
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
