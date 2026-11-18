"""
high_score.py — Save and load the high score for SnakeGH.

The high score is stored in a plain text file so it survives between
game sessions.  This module provides two simple functions: one to read
the saved score and one to write a new one.
"""

from constants import HIGH_SCORE_FILE


def load_high_score():
    """Read the saved high score from disk, or return 0 if none exists yet.

    The file contains a single integer.  If the file is missing or
    contains garbage, we safely fall back to 0.

    Returns
    -------
    int
        The previous high score (0 if the file doesn't exist).
    """
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_high_score(score):
    """Write *score* to the high-score file, overwriting any previous value.

    Parameters
    ----------
    score : int
        The new high score to persist.
    """
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))
