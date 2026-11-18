"""
special_food.py — Special food logic for SnakeGH.

This module manages a special, bonus food item that appears randomly
after the snake eats regular food. The special food is worth more points
(3 instead of 1) but disappears after a short time (5 seconds by default).

How it works:
  1. After eating regular food, there's a chance (50%) that special food
     will appear at a random empty cell on the board.
  2. A timer starts counting down from SPECIAL_FOOD_LIFETIME (5 seconds).
  3. If the snake eats the special food before it expires, the player
     gets 3 bonus points.
  4. If the timer runs out, the special food disappears and won't appear
     again until the next regular food is eaten.

This module tracks:
  - special_food: the (x, y) position of the special food, or None if
    no special food is currently on the board.
  - expires_at: the time (in milliseconds) when the special food will
    disappear, compared against the current time each tick.
"""

import random
import time

from constants import COLS, ROWS


# ==================================================================
# Configuration — change these to adjust the special food behaviour
# ==================================================================

SPECIAL_FOOD_LIFETIME = 5000   # How long the special food stays, in ms (5 seconds).
SPECIAL_FOOD_CHANCE   = 0.5    # Probability (0.0 to 1.0) that special food
                               # appears after eating regular food (50% chance).
SPECIAL_FOOD_POINTS   = 3      # Bonus points awarded when eating special food.


# ==================================================================
# State variables
# ==================================================================

special_food = None             # Current position (x, y) or None if not present.
expires_at   = 0                # Timestamp (ms) when the special food expires.


# ------------------------------------------------------------------
# Initialise / reset
# ------------------------------------------------------------------

def reset():
    """Clear any existing special food.

    Called when a new game starts to ensure no leftover special food
    from the previous game remains.
    """
    global special_food, expires_at
    special_food = None
    expires_at = 0


# ------------------------------------------------------------------
# Spawn special food
# ------------------------------------------------------------------

def maybe_spawn(snake):
    """Decide whether to spawn special food after eating regular food.

    Uses a random chance (SPECIAL_FOOD_CHANCE) to determine if special
    food appears. If it does, picks a random empty cell and sets the
    expiry timer.

    Parameters
    ----------
    snake : list[tuple[int, int]]
        Current snake body positions (to avoid placing food on the snake).

    Returns
    -------
    bool
        True if special food was spawned, False otherwise.
    """
    global special_food, expires_at

    # Roll the dice — only spawn with the configured chance.
    if random.random() > SPECIAL_FOOD_CHANCE:
        special_food = None
        expires_at = 0
        return False

    # Pick a random empty cell for the special food.
    free = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in snake]
    if not free:
        special_food = None
        return False

    special_food = random.choice(free)

    # Set the expiry time: current time + lifetime in milliseconds.
    expires_at = int(time.time() * 1000) + SPECIAL_FOOD_LIFETIME

    return True


# ------------------------------------------------------------------
# Check expiry
# ------------------------------------------------------------------

def is_expired():
    """Check whether the special food has expired.

    Compares the current time with the expiry time. If the special food
    has expired, it is automatically removed.

    Returns
    -------
    bool
        True if the special food has expired (or is not present).
    """
    global special_food, expires_at

    if special_food is None:
        return True

    current_time = int(time.time() * 1000)
    if current_time >= expires_at:
        # Time's up — remove the special food.
        special_food = None
        expires_at = 0
        return True

    return False


# ------------------------------------------------------------------
# Get remaining time
# ------------------------------------------------------------------

def remaining_time():
    """Return how many seconds are left before the special food expires.

    Returns
    -------
    float
        Seconds remaining (0 if no special food or already expired).
    """
    if special_food is None:
        return 0.0

    current_time = int(time.time() * 1000)
    remaining_ms = expires_at - current_time
    return max(0.0, remaining_ms / 1000.0)


# ------------------------------------------------------------------
# Check if a position matches the special food
# ------------------------------------------------------------------

def at_position(pos):
    """Check if a given position is where the special food is located.

    Parameters
    ----------
    pos : tuple[int, int]
        The (x, y) position to check.

    Returns
    -------
    bool
        True if *pos* matches the special food location.
    """
    return special_food is not None and pos == special_food


# ------------------------------------------------------------------
# Consume the special food
# ------------------------------------------------------------------

def consume():
    """Remove the special food after the snake eats it.

    Returns
    -------
    int
        The bonus points awarded (SPECIAL_FOOD_POINTS).
    """
    global special_food, expires_at
    points = SPECIAL_FOOD_POINTS
    special_food = None
    expires_at = 0
    return points
