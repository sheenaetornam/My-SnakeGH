"""
constants.py — All game-wide constants for SnakeGH.

This file holds every fixed value the game needs: board size, cell size,
speed settings, colours, and the high-score file name.
By putting them here in one place, every other module can import what it
needs without duplicating numbers.  If you ever want to make the board
bigger or the game faster, you only change it here.
"""

# ---- Board geometry ----
CELL = 24                 # Size of one square on the board, in pixels.
COLS = 25                 # Number of squares across (width in cells).
ROWS = 20                 # Number of squares down   (height in cells).

# Pixel dimensions derived from the cell size.
WIDTH  = CELL * COLS      # 600 pixels  (24 × 25)
HEIGHT = CELL * ROWS      # 480 pixels  (24 × 20)

# ---- Speed / timing ----
START_SPEED = 150         # Milliseconds between each game tick at level 1.
                          # Smaller numbers mean the snake moves faster.
MIN_SPEED   = 60          # The fastest the game can ever go (ms per tick).
SPEED_STEP  = 15          # How many ms faster each new level makes the game.

# ---- Scoring ----
LEVEL_UP_EVERY = 5        # Points needed before the level goes up by 1.

# ---- High-score file ----
HIGH_SCORE_FILE = "snake_highscore.txt"   # Text file that persists the best score.

# ---- Colours (hex strings) ----
BG_COLOUR       = "#0d1b2a"   # Dark navy — window background.
CANVAS_COLOUR   = "#121212"   # Almost black — game board background.
GRID_COLOUR     = "#1e1e1e"   # Very dark grey — faint grid lines.
SNAKE_HEAD      = "#1b5e20"   # Dark green — the head of the snake.
SNAKE_BODY      = "#43a047"   # Medium green — the body segments.
FOOD_COLOUR     = "#e53935"   # Red — the regular food dot.
SPECIAL_FOOD    = "#ffd700"   # Gold — the special bonus food (rarer, worth more).
TITLE_COLOUR    = "#66bb6a"   # Light green — the "SnakeGH" title.
TEXT_COLOUR     = "white"     # White — score text and messages.
SUB_COLOUR      = "#bbbbbb"   # Light grey — subtitle / hint text.
HINT_COLOUR     = "#90a4ae"   # Blue-grey — control hints at the bottom.

# ---- Direction helpers ----
# Each direction maps to (dx, dy) — how much the head's (x, y) changes.
DIRECTIONS = {
    "Up":    (0, -1),
    "Down":  (0,  1),
    "Left":  (-1, 0),
    "Right": (1,  0),
}

# Opposite directions — used to prevent the snake from reversing into itself.
OPPOSITE = {
    "Up": "Down",
    "Down": "Up",
    "Left": "Right",
    "Right": "Left",
}

# Keyboard key names (lowercase) mapped to direction strings.
# Supports both Arrow keys and WASD.
KEYS = {
    "up":   "Up",
    "w":    "Up",
    "down": "Down",
    "s":    "Down",
    "left": "Left",
    "a":    "Left",
    "right":"Right",
    "d":    "Right",
}
