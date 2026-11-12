# Zombie Joe

## Working mode (overrides my global CLAUDE.md)

This project is NOT a learning project. Ignore the "Learning Mode" rules in my global `~/.claude/CLAUDE.md` while working here:

- Write and edit code directly. No need to ask first or give hints instead of code.
- Don't suggest Anki cards or quiz me unless I ask.
- Still keep code simple and readable, and briefly call out anything non-obvious or anything I should double-check.
- Commit or push only when I ask.

## Roadmap

See @TODO.md. Work on one task at a time, in order.
When a task's "Done when" is met, check it off and stop so I can test.
Terms: "town" = one map; "stage" = one round of waves played in a town; "player level" = XP level.
Don't add new dependencies without asking.

## The game

A 2D top-down zombie shooter in Python. Joe moves around his town killing zombies.

- Each stage is a series of zombie waves; each wave gets a bit harder (more zombies and/or faster).
- One difficulty setting: the game simply gets harder as you progress.
- Joe starts with a pistol (one shot at a time, with a delay, unlimited ammo). Other guns are picked up inside houses (none in town 1) and use ammo from pickups.
- Houses can be entered: walking through a door switches to that house's interior map.
- Each town is its own map. A roadblock ("Not available yet") blocks the road to the next town until that town's stages are cleared.
- Kills give XP; player levels raise stats.
- Players have 3 lives (hearts). Losing all HP costs a life and restarts the current stage. Losing the last life sends Joe back to the previous stage (never into a previous town) with full lives and the guns he had when that stage started.
- Guns with limited ammo reload automatically when empty; reload time is set per gun.
- 1 or 2 players (local co-op later, shared screen). Online play may come later.

## Tech stack

- Python 3, `pygame-ce` (imported as `pygame`), `pytmx` for loading Tiled maps
- Maps are made in Tiled and saved as `.tmx` in `maps/`
- Dependencies in `requirements.txt`; use a venv at `.venv/`

## Project layout

- `main.py`: entry point, creates `Game` and runs it
- `game/`: all game code, one main class per file (`player.py`, `zombie.py`, `weapon.py`, `bullet.py`, `effects.py`, `stage.py`, `camera.py`, `hud.py`, `controls.py`, `save.py`, `settings.py`, `game.py`)
- `data/`: JSON stats (player, weapons, zombies, stages, controls)
- `maps/`: Tiled `.tmx` maps and `.tsx` tilesets
- `assets/`: images, sounds, fonts
- `saves/`: runtime save files (gitignored)

## Conventions

- **Support multiple players everywhere.** Keep players in a list and never assume there's a single player. Zombies target the nearest player; the camera and HUD handle 1–2 players.
- **`Player` never reads the keyboard directly.** `controls.py` turns input into actions per player and passes them to `Player`, so input can later come from a controller or the network.
- **Gameplay numbers live in `data/*.json`**, not in code (damage, fire rate, zombie speed/health, wave sizes, how many stages unlock each town).
- **Constants live in `game/settings.py`** (screen size, FPS, tile size, colors).
- Use frame-rate-independent movement (multiply by delta time).
- Build features incrementally and keep the game runnable after each change.

## Running

```
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
