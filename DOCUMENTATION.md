# SnakeGH — Documentation

## What is SnakeGH?

SnakeGH is a classic **Snake arcade game** built with Python and Tkinter. The snake moves around a grid, eating food to grow longer and score points. The game gets faster as you level up. If the snake hits a wall or its own body, the game ends.

This documentation explains **how the game works**, **how each file contributes**, and **how everything connects** to make the game active and playable.

---

## How to Run the Game

Open a terminal in the project folder and run:

```
python SnakeGH.py
```

This opens a window where you can play the game using your keyboard.

---

## Controls

| Key | Action |
|-----|--------|
| **Arrow keys** or **W / A / S / D** | Change the snake's direction |
| **Space** | Start a new game or restart after game over |
| **P** | Pause or resume the game |

---

## Project Structure (9 Files)

The project is split into **9 Python files**, each with a clear, single responsibility. This is called **separation of concerns** — each file does one job well, which makes the code easier to read, test, and modify.

```
SnakeGH/
├── SnakeGH.py         # Main entry point — starts everything
├── constants.py       # All fixed values (sizes, colours, speeds)
├── logic.py           # Pure game rules (movement, collisions, scoring)
├── high_score.py      # Save and load the best score from a file
├── game.py            # Game state + the game loop (the brain)
├── gui.py             # Window, canvas, drawing, keyboard input
├── sounds.py          # Sound effects for eating, leveling up, game over
├── special_food.py    # Bonus food that appears and disappears
└── eyes.py            # Draws eyes on the snake's head
```

---

## File-by-File Breakdown

### 1. `SnakeGH.py` — The Entry Point

**Role:** This is the file you run to start the game. It connects all the other modules together.

**What it does step by step:**

1. **Imports** all modules (`gui`, `game`, `sounds`, `special_food`, `eyes`, `constants`).
2. **Wires callbacks** — `game.py` needs to call drawing functions from `gui.py`, but importing them directly would cause a circular import. So `SnakeGH.py` acts as the middleman, passing the references after both modules are loaded.
3. **Builds the window** by calling `gui.build_window()`.
4. **Initialises the game** by calling `game.init_game()`.
5. **Draws the start screen** showing "Press Space to start".
6. **Starts the event loop** with `root.mainloop()` — this keeps the window open and waiting for your input.

**Key concept:** `root.mainloop()` is the Tkinter event loop. It runs forever, processing key presses and scheduling game ticks. Without it, the window would flash and close immediately.

---

### 2. `constants.py` — All Fixed Values

**Role:** Every number, colour, and mapping that never changes during the game lives here.

**Why a separate file?** If you want to make the board bigger, change the colours, or adjust the speed, you only edit this one file instead of hunting through every file.

**Key constants:**

| Constant | Value | Meaning |
|----------|-------|---------|
| `CELL` | 24 | Size of one grid square in pixels |
| `COLS` | 25 | Number of columns (width in cells) |
| `ROWS` | 20 | Number of rows (height in cells) |
| `WIDTH` | 600 | Canvas width in pixels (24 × 25) |
| `HEIGHT` | 480 | Canvas height in pixels (24 × 20) |
| `START_SPEED` | 150 | Milliseconds per tick at level 1 |
| `MIN_SPEED` | 60 | Fastest possible speed (ms per tick) |
| `SPEED_STEP` | 15 | How many ms faster per level |
| `LEVEL_UP_EVERY` | 5 | Points needed to level up |

**Direction helpers:**

- `DIRECTIONS` — Maps `"Up"`, `"Down"`, `"Left"`, `"Right"` to `(dx, dy)` coordinate changes.
- `OPPOSITE` — Maps each direction to its opposite (used to prevent 180° reversal).
- `KEYS` — Maps keyboard keys (arrows + WASD) to direction names.

---

### 3. `logic.py` — Pure Game Rules

**Role:** The "brain" of the game. It knows the rules but has **no GUI code** — it only takes data in and returns data out.

**Functions:**

| Function | What it does |
|----------|-------------|
| `next_head(head, direction)` | Calculates where the snake's head moves next. For example, if the head is at `(5, 10)` and direction is `"Right"`, it returns `(6, 10)`. |
| `hits_wall(cell)` | Returns `True` if a cell is outside the board boundaries (x < 0, x >= 25, y < 0, or y >= 20). |
| `hits_self(head, snake)` | Returns `True` if the head collides with any body segment. It skips the last tail segment because the tail moves forward each tick. |
| `random_food(snake)` | Picks a random empty cell (not occupied by the snake) for the food. |
| `level_for(score)` | Calculates the current level. Every 5 points, the level goes up by 1. |
| `speed_for(level)` | Calculates milliseconds per tick. Each level makes the game 15ms faster, down to a minimum of 60ms. |

**Why "pure" matters:** Since these functions don't touch the GUI, they can be tested independently. You can call `next_head((5, 10), "Right")` from a Python shell and get `(6, 10)` without needing a window.

---

### 4. `high_score.py` — Persistent Best Score

**Role:** Saves and loads the best score to/from a text file (`snake_highscore.txt`) so it survives between game sessions.

**Functions:**

| Function | What it does |
|----------|-------------|
| `load_high_score()` | Reads the file and returns the saved score as an integer. Returns `0` if the file doesn't exist or is empty. |
| `save_high_score(score)` | Writes the new high score to the file, overwriting the old value. |

**How it works:** When the game starts, `load_high_score()` reads the best score. When the game ends, if the current score beats the high score, `save_high_score()` writes the new best.

---

### 5. `game.py` — Game State and Game Loop

**Role:** This is the **heart of the game**. It owns all the changing data (snake position, score, direction) and runs the game loop that updates everything every tick.

**Global state variables:**

| Variable | Type | Meaning |
|----------|------|---------|
| `snake` | list of (x, y) | The snake's body. Index 0 is the head. |
| `direction` | string | Current movement direction. |
| `next_direction` | string | Direction queued by the player this tick. |
| `food` | (x, y) | Position of the regular food. |
| `score` | int | Current score. |
| `level` | int | Current level. |
| `running` | bool | `True` while the game is active. |
| `paused` | bool | `True` when the player pressed Pause. |
| `loop_id` | int | Tkinter's handle for the next scheduled tick. |

**Functions:**

| Function | What it does |
|----------|-------------|
| `init_game()` | Resets all variables to starting values. Called once at program start. |
| `start_game(root)` | Resets the board and starts the game loop. Called when Space is pressed. |
| `change_direction(new_dir)` | Queues a new direction, preventing 180° reversal. |
| `toggle_pause(root)` | Pauses or resumes the game loop. |
| `_tick()` | **The core game loop** — called every tick (see below). |
| `_game_over()` | Handles game over: plays sound, saves high score, shows message. |

---

### ⭐ The Game Loop (`_tick()`) — How the Game Stays Active

This is the most important function in the entire project. It runs every few milliseconds (starting at 150ms) and does the following steps:

```
Step 1: Commit the queued direction
        direction = next_direction

Step 2: Calculate the new head position
        head = next_head(snake[0], direction)

Step 3: Check for collisions
        If the head hits a wall or its own body → Game Over

Step 4: Check for regular food
        If head == food:
            - Add 1 point
            - Grow the snake (add head, don't remove tail)
            - Place new food
            - Play eat sound
            - Check for level up → play level-up sound
            - Try to spawn special food

Step 5: Check for special food
        If head is on special food (and not expired):
            - Add 3 bonus points
            - Grow the snake
            - Play special food sound

Step 6: Normal move (no food eaten)
        Add the new head, remove the tail

Step 7: Redraw the screen
        gui_draw()

Step 8: Schedule the next tick
        root.after(speed_for(level), _tick)
```

**The scheduling trick:** `root.after(milliseconds, function)` is a Tkinter method that schedules a function to be called after a delay. At the end of each `_tick()`, it schedules the *next* `_tick()`, creating a continuous loop. The delay gets shorter as the level increases, making the game faster.

---

### 6. `gui.py` — Window, Drawing, and Input

**Role:** Everything visual. It creates the Tkinter window, draws the snake and food on a canvas, and handles keyboard input.

**Key components created by `build_window()`:**

1. **Main window** — A Tkinter `Tk` window titled "SnakeGH".
2. **Title label** — Shows "SnakeGH" in large green text.
3. **Score label** — Shows current score, level, and best score.
4. **Game canvas** — A 600×480 pixel drawing area where the game happens.
5. **Control hints** — Text at the bottom showing the keyboard controls.

**Functions:**

| Function | What it does |
|----------|-------------|
| `build_window()` | Creates the entire window layout and returns the root window. |
| `draw_grid()` | Draws faint grid lines once at startup. |
| `draw()` | Called every tick. Clears the old snake and food, then redraws them in their new positions. Also draws special food and the snake's eyes. |
| `update_labels()` | Refreshes the score/level/best label. |
| `show_message(title, subtitle)` | Draws a centred overlay message (start screen, game over, pause). |
| `on_key(event)` | Handles every key press: arrows/WASD for direction, Space for start/restart, P for pause. |

**Drawing order in `draw()`:**

1. Delete old snake and food shapes (using tags).
2. Draw the regular food as a red circle.
3. Draw the special food as a gold circle with a ★ symbol (if present).
4. Draw each snake segment as a green rectangle (darker for the head).
5. Draw the snake's eyes on the head.
6. Update the score label.

---

### 7. `sounds.py` — Sound Effects

**Role:** Plays short sound effects using Windows' built-in `winsound` module.

**How it works:** `winsound.Beep(frequency, duration)` plays a tone at a specific pitch (frequency in Hz) for a specific time (duration in ms). By combining multiple beeps with different pitches, we create distinct sounds.

| Function | Sound | How it's made |
|----------|-------|---------------|
| `eat_food()` | Quick "chomp" | One beep at 600 Hz for 80ms |
| `eat_special_food()` | Rising "power-up" | Two beeps: 800 Hz → 1200 Hz (pitch goes up) |
| `game_over()` | Sad descending melody | Three beeps: 400 Hz → 300 Hz → 200 Hz (pitch goes down) |
| `level_up()` | Cheerful fanfare | Three beeps: 500 Hz → 700 Hz → 900 Hz (pitch goes up) |

**When sounds play:**

- **Eat food:** When the snake eats regular food in `_tick()`.
- **Eat special food:** When the snake eats the gold bonus food.
- **Level up:** When the score crosses a level boundary.
- **Game over:** When the snake crashes into a wall or itself.

---

### 8. `special_food.py` — Bonus Food Feature

**Role:** Manages a special gold food that appears randomly after eating regular food and disappears after 5 seconds.

**Configuration:**

| Setting | Value | Meaning |
|---------|-------|---------|
| `SPECIAL_FOOD_LIFETIME` | 5000 ms | How long the special food stays on the board |
| `SPECIAL_FOOD_CHANCE` | 0.5 (50%) | Probability it appears after eating regular food |
| `SPECIAL_FOOD_POINTS` | 3 | Bonus points when eaten (vs 1 for regular food) |

**Functions:**

| Function | What it does |
|----------|-------------|
| `reset()` | Clears any existing special food. Called at game start. |
| `maybe_spawn(snake)` | Decides whether to spawn special food (50% chance). If yes, picks a random empty cell and sets a 5-second timer. |
| `is_expired()` | Checks if the 5-second timer has run out. If expired, removes the food. |
| `at_position(pos)` | Checks if a given position matches the special food's location. |
| `consume()` | Removes the special food and returns the bonus points (3). |

**How it works in the game:**

1. After eating regular food, `maybe_spawn()` is called.
2. With 50% chance, a gold food appears at a random empty cell.
3. A timer starts counting down from 5 seconds.
4. If the snake reaches it in time → +3 points and a special sound.
5. If 5 seconds pass → the food disappears.

---

### 9. `eyes.py` — Snake Eyes Feature

**Role:** Draws two eyes (white circle + black pupil) on the snake's head so it looks like a real snake with a face.

**How it works:** The eyes reposition based on the current direction:

| Direction | Eye Position |
|-----------|-------------|
| **Right** | On the right side of the head, side by side |
| **Left** | On the left side of the head, side by side |
| **Up** | On the top side of the head, one above the other |
| **Down** | On the bottom side of the head, one above the other |

This means the snake always appears to be **looking where it's going**.

**Function:**

| Function | What it does |
|----------|-------------|
| `draw_eyes(canvas, head_x, head_y, direction)` | Calculates the two eye positions based on direction and draws each eye as a white circle with a black pupil. |

---

## How the Modules Connect (Data Flow)

```
                    ┌─────────────┐
                    │ SnakeGH.py  │  ← You run this file
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │  gui.py  │ │ game.py  │ │constants │
        └────┬─────┘ └────┬─────┘ └────┬─────┘
             │            │            │
             │     ┌──────┴──────┐     │
             │     ▼             ▼     │
             │  logic.py   high_score  │
             │             sounds.py   │
             │             special_    │
             │             food.py     │
             │             eyes.py     │
             │                         │
             └─────┬───────────────────┘
                   │
              Drawing on
              the canvas
              every tick
```

**Import chain:**

1. `SnakeGH.py` imports everything.
2. `game.py` imports from `logic.py`, `high_score.py`, `sounds.py`, `special_food.py`.
3. `gui.py` imports from `constants.py`, `eyes.py`, `special_food.py`.
4. `logic.py` imports from `constants.py`.
5. `eyes.py` imports from `constants.py`.
6. `special_food.py` imports from `constants.py`.

**Callback wiring (avoids circular imports):**

- `game.py` does NOT import `gui.py` directly.
- Instead, `SnakeGH.py` sets `game.gui_draw = gui.draw` after both are loaded.
- This way, `game.py` can call `gui_draw()` without creating a circular dependency.

---

## The Complete Game Lifecycle

Here's what happens from start to finish:

### Phase 1: Startup
1. You run `python SnakeGH.py`.
2. All modules are imported.
3. `gui.build_window()` creates the window, canvas, and labels.
4. `game.init_game()` resets the snake to 3 segments at `[(5,10), (4,10), (3,10)]`.
5. The start screen is drawn: "SnakeGH — Press Space to start".
6. `root.mainloop()` starts the event loop, waiting for input.

### Phase 2: Player Presses Space
1. `on_key()` detects Space and calls `start_game(root)`.
2. The snake is reset, score is 0, level is 1.
3. `root.after(150, _tick)` schedules the first game tick.

### Phase 3: The Game Loop (repeating every tick)
1. `_tick()` moves the snake one cell in the current direction.
2. Collision check: wall or self → `_game_over()`.
3. Food check: regular food → grow, score +1, play sound, maybe spawn special food.
4. Special food check → grow, score +3, play special sound.
5. Normal move → add head, remove tail.
6. `gui.draw()` redraws everything.
7. `root.after(speed, _tick)` schedules the next tick.

### Phase 4: Game Over
1. Snake hits a wall or itself.
2. `sounds.game_over()` plays the sad melody.
3. High score is checked and saved if beaten.
4. "Game Over!" message is displayed.
5. Player presses Space to restart → back to Phase 2.

---

## Key Programming Concepts Used

### Separation of Concerns
Each file has one clear job. The logic file doesn't know about the GUI. The GUI doesn't know about the rules. This makes the code easy to change — for example, you could replace the Tkinter GUI with a different one without touching the game logic.

### The Game Loop Pattern
Most games use a loop that repeats: **update state → check conditions → draw → schedule next frame**. Our `_tick()` function follows this exact pattern.

### Event-Driven Programming
Tkinter is event-driven: instead of polling for input, it calls `on_key()` whenever a key is pressed. Similarly, `root.after()` calls `_tick()` when the timer expires.

### Callback Pattern
`game.py` calls `gui_draw()` without importing `gui.py`. The callback is wired in `SnakeGH.py`. This avoids circular imports where A imports B and B imports A.

### Pure Functions
`logic.py` contains pure functions: same input always gives the same output, with no side effects. This makes them easy to test and reason about.

---

## Customization Guide

Want to change something? Here's where to look:

| Want to... | Edit this file | Change this... |
|------------|---------------|----------------|
| Make the board bigger | `constants.py` | `COLS`, `ROWS`, `CELL` |
| Change the colours | `constants.py` | Any `*_COLOUR` constant |
| Make the game faster/slower | `constants.py` | `START_SPEED`, `MIN_SPEED`, `SPEED_STEP` |
| Change level-up frequency | `constants.py` | `LEVEL_UP_EVERY` |
| Change special food behaviour | `special_food.py` | `SPECIAL_FOOD_LIFETIME`, `SPECIAL_FOOD_CHANCE`, `SPECIAL_FOOD_POINTS` |
| Change the sounds | `sounds.py` | Frequency and duration in each `Beep()` call |
| Change the eye size | `eyes.py` | `EYE_RADIUS`, `PUPIL_RADIUS` |

---

## Summary

SnakeGH is built from **9 files** that work together:

- **`SnakeGH.py`** starts everything and connects the pieces.
- **`constants.py`** holds all the fixed numbers and colours.
- **`logic.py`** knows the rules (movement, collisions, scoring).
- **`high_score.py`** saves the best score to a file.
- **`game.py`** runs the game loop, the heart of the game.
- **`gui.py`** draws everything and handles keyboard input.
- **`sounds.py`** plays sound effects for game events.
- **`special_food.py`** manages the bonus gold food.
- **`eyes.py`** draws eyes on the snake's head.

The game stays active through a **game loop** that runs every few milliseconds, updating the snake's position, checking for collisions and food, redrawing the screen, and scheduling the next tick. The loop gets faster as you level up, making the game more challenging.
