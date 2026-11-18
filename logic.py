"""
logic.py — Pure game-logic functions for SnakeGH.

These functions do NOT touch the GUI.  They only take data in and return
data out, which makes them easy to test and reason about.  Think of this
file as the "brain" of the game: it knows the rules but doesn't know
anything about windows, buttons, or colours.
"""

import random

from constants import COLS, ROWS, DIRECTIONS, LEVEL_UP_EVERY, START_SPEED, MIN_SPEED, SPEED_STEP


# ------------------------------------------------------------------
# Movement
# ------------------------------------------------------------------

def next_head(head, direction):
    """Return the new (x, y) the head moves into when going *direction*.

    Parameters
    ----------
    head : tuple[int, int]
        The current (x, y) of the snake head.
    direction : str
        One of "Up", "Down", "Left", "Right".

    Returns
    -------
    tuple[int, int]
        The new (x, y) after moving one cell.

    Example
    -------
    >>> next_head((5, 10), "Right")
    (6, 10)
    """
    dx, dy = DIRECTIONS[direction]       # e.g. "Right" → (1, 0)
    x, y = head
    return (x + dx, y + dy)


# ------------------------------------------------------------------
# Collision checks
# ------------------------------------------------------------------

def hits_wall(cell):
    """Return True if *cell* is outside the board boundaries.

    The board columns run from 0 to COLS-1 and rows from 0 to ROWS-1.
    Anything outside that range is a wall.

    Parameters
    ----------
    cell : tuple[int, int]
        The (x, y) to check.

    Returns
    -------
    bool
        True when the cell is outside the board.
    """
    x, y = cell
    return x < 0 or x >= COLS or y < 0 or y >= ROWS


def hits_self(head, snake):
    """Return True if *head* collides with the snake's own body.

    We skip the very last tail segment (snake[-1]) because it will move
    forward this tick, so it won't actually be there when the head arrives.

    Parameters
    ----------
    head : tuple[int, int]
        The new head position.
    snake : list[tuple[int, int]]
        The full snake body (head first, tail last).

    Returns
    -------
    bool
        True when the head runs into any body segment.
    """
    return head in snake[:-1]            # skip the tail — it moves away


# ------------------------------------------------------------------
# Food placement
# ------------------------------------------------------------------

def random_food(snake):
    """Pick a random empty square on the board for the food.

    Builds a list of every cell NOT occupied by the snake, then picks
    one at random.

    Parameters
    ----------
    snake : list[tuple[int, int]]
        Current snake body positions.

    Returns
    -------
    tuple[int, int]
        A random (x, y) that is not in *snake*.
    """
    # Build a list of all free cells.
    free = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in snake]
    return random.choice(free)


# ------------------------------------------------------------------
# Level & speed helpers
# ------------------------------------------------------------------

def level_for(score):
    """Calculate the current level from the score.

    The level goes up by 1 every LEVEL_UP_EVERY points (default: 5).

    Parameters
    ----------
    score : int
        The current score.

    Returns
    -------
    int
        The level number (starts at 1).

    Example
    -------
    >>> level_for(0)
    1
    >>> level_for(5)
    2
    >>> level_for(12)
    3
    """
    return score // LEVEL_UP_EVERY + 1


def speed_for(level):
    """Calculate the milliseconds-per-tick for a given level.

    Each level makes the game SPEED_STEP ms faster, but never faster than
    MIN_SPEED ms.

    Parameters
    ----------
    level : int
        The current level.

    Returns
    -------
    int
        Milliseconds between game ticks.

    Example
    -------
    >>> speed_for(1)
    150
    >>> speed_for(2)
    135
    """
    return max(MIN_SPEED, START_SPEED - (level - 1) * SPEED_STEP)
