# Zombie Joe Roadmap

One task at a time, in order. Each task's **Done when** is something you can check by playing.
Terms: **town** = one map; **stage** = one round of waves played in a town; **player level** = XP level.

## Controls (current)

| Action | Keys |
|---|---|
| Move | WASD or arrow keys |
| Shoot | Space (fires the way Joe last walked) |
| Quit | Esc |

Run with `python main.py`. Keys can be changed in `data/controls.json`.

## M0 Setup

- [x] Window and game loop (60 FPS, delta time, Esc/close to quit)
  - Done when: `python main.py` opens a window and closes cleanly.
- [x] Folder structure (`game/`, `data/`, `maps/`, `assets/`, `saves/`)
  - Done when: the folders match the layout in CLAUDE.md.
- [x] Player character and movement (WASD or arrows, no faster on diagonals)
  - Done when: Joe moves smoothly in all 8 directions.

## M1 Boundaries and shooting

- [x] Screen boundaries: Joe can't leave the window (until the Tiled map replaces this)
  - Done when: walking into any edge stops Joe with him still fully visible.
- [x] Pistol: each press of Space fires one small yellow bullet the way Joe is walking; presses during the fire delay are ignored
  - Done when: mashing Space can't fire faster than the delay set in `data/weapons.json`, and holding it fires only once.
- [x] Bullets hitting a wall (the screen edge for now) make a small explosion; bullets that reach max range just vanish
  - Done when: shooting at an edge shows a quick spark burst where the bullet hits.
- [x] HUD in the top right: weapon name and ammo (∞ for the pistol, `in magazine/reserve` like `30/100` for other guns), red health bar, hearts for lives
  - Done when: the HUD shows "Pistol ∞", a full red bar, and 3 red hearts.

## M2 Zombies

- [x] Zombies (grey squares for now) spawn just off-screen and slowly walk toward the nearest player
  - Done when: zombies appear from the edges and follow Joe as he moves.
- [x] Zombie health: bullets damage zombies and are used up on hit; each hit sprays a little red blood; at 0 HP the zombie stops and slowly crumbles away
  - Done when: a zombie takes 2 pistol hits to die (set by `health` in `data/zombies.json` and pistol `damage`), bleeds on each hit, and disintegrates on death.
- [ ] Swap the grey squares for a zombie image once one is in `assets/images/zombies/`
  - Done when: zombies show the image and turn to face the way they walk.
- [ ] Zombies don't stack into one blob (they push apart a little)
  - Done when: a crowd of zombies stays spread out instead of overlapping.

## M3 Player health and game over

- [ ] Zombies hurt Joe on contact, with a short invulnerability window after each hit
  - Done when: touching a zombie lowers HP once per second at most, and Joe flashes while invulnerable.
- [ ] Dying costs a life: at 0 HP, a heart turns grey and the current stage restarts from wave 1 with full HP (once XP exists in M6, XP also resets to what Joe had at the start of the stage, so dying can't farm XP)
  - Done when: dying shows one fewer red heart and restarts the stage. (Until stages exist in M4, "restart" means: clear the zombies and put Joe back in the middle.)
- [ ] Game over when the last life is lost: show GAME OVER and "press R to continue"; R sends Joe back to the **previous stage** (but never into a previous town: on a town's first stage, he restarts that stage) with full lives and the guns/ammo he had when that stage started
  - Done when: losing the third life on stage 3 shows GAME OVER, and R starts stage 2 with 3 hearts. (Until stages exist in M4, R just restarts with 3 hearts; check the "previous stage" part again after M4.)

## M4 Waves

- [ ] Waves from `data/stages.json`: each wave spawns a set number of zombies; the next wave starts after a short break once all are dead
  - Done when: killing every zombie shows "Wave 2" and a new, larger wave arrives.
- [ ] Waves scale up: more zombies and/or a bit faster each wave (both set in JSON)
  - Done when: later waves are noticeably harder, and changing the JSON changes it.
- [ ] Stage clear: after the last wave, show "Stage cleared" and start the next stage, which is harder than the last
  - Done when: clearing the final wave shows the message and stage 2 begins with tougher waves.

## M5 HUD

- [ ] Add wave number and stage number to the HUD (HP, ammo and lives are already there)
  - Done when: both are on screen and update during play.

## M6 Player levels (XP)

- [ ] Kills give XP; XP thresholds for each player level live in `data/player.json`
  - Done when: killing zombies fills an XP bar and shows "Level up!" at the threshold.
- [ ] Level-ups raise stats by amounts set in JSON (**which stats: TBD**, decide before starting this task)
  - Done when: after a level-up, the chosen stats are visibly better.

## M7 Tiled map and camera

- [ ] Load and draw a Tiled town map (`.tmx`) that is bigger than the screen
  - Done when: the town map draws under Joe instead of the plain background.
- [ ] Camera follows Joe and stops at the map edges
  - Done when: walking around scrolls the map, and the view never shows past the map edge.
- [ ] Wall collision from a Tiled collision layer (replaces screen boundaries)
  - Done when: Joe can't walk through buildings or walls, and slides along them instead of sticking.
- [ ] Object layer: player spawn and zombie spawn points come from the map
  - Done when: Joe starts at the spawn point and zombies come from the spawn points placed in Tiled.

## M8 Houses and guns

- [ ] Doors: walking into a house door switches to that house's interior map; the exit door goes back outside
  - Done when: Joe can go in and out of a house and comes out at the same door.
- [ ] Gun pickups inside houses (none in town 1); walking over one picks it up
  - Done when: in town 2, a house has a gun Joe can pick up, and town 1 has none.
- [ ] Switch weapons (e.g. Q or number keys); each gun's damage, fire delay and ammo come from `data/weapons.json`
  - Done when: Joe can switch between the pistol and a picked-up gun, and they feel different.
- [ ] Ammo: picked-up guns run out and can't fire at 0 ammo (the pistol stays unlimited)
  - Done when: a picked-up gun stops firing when empty, and the pistol never runs out.
- [ ] Automatic reloading: when the magazine is empty, the gun reloads from reserve ammo after a short delay (`reload_time` per gun in `data/weapons.json`); it can't fire while reloading, and the HUD shows "Reloading..."
  - Done when: emptying a gun shows "Reloading...", and after that gun's reload time the HUD goes from `0/100` to `30/70`.
- [ ] Ammo pickups found in the world refill that gun's rounds
  - Done when: walking over an ammo pickup adds rounds to the matching gun.
- [ ] Save a snapshot of Joe's guns and ammo at the start of each stage, so game over can restore them
  - Done when: picking up a gun mid-stage and then getting a game over leaves Joe without that gun.

## M9 Towns and roadblocks

- [ ] Roadblock on the road out of town; touching it shows "Not available yet"
  - Done when: walking into the roadblock stops Joe and shows the warning.
- [ ] The roadblock disappears after the town's stages are cleared (count set in JSON)
  - Done when: after the last stage in town 1, the roadblock is gone.
- [ ] Walking down the open road loads the next town map, with harder stages
  - Done when: leaving town 1 loads town 2, and its waves start tougher than town 1's.

## M10 Polish

- [ ] Start menu (Play, Quit), sharing code with the game over screen
  - Done when: the game opens to a menu and Play starts a run.
- [ ] Sound effects: gunshot, zombie hit, zombie death, player hurt
  - Done when: each action plays its sound.
- [ ] Save progress (town, stage, player level, guns) to `saves/`; Continue on the start menu
  - Done when: quitting and choosing Continue picks up at the same town and stage with the same guns and level.

## M11 Co-op (later)

- [ ] Second player joins on the start menu (WASD and arrows split, using the existing co-op controls)
  - Done when: two players move and shoot on the same screen.
- [ ] Camera keeps both players in view; HUD shows both players' HP and XP
  - Done when: both players stay on screen and each has their own HUD.

## Later ideas

- Online play
- Gamepad controls
