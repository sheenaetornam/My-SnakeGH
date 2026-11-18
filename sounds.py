"""
sounds.py — Sound effects for SnakeGH.

This module plays short sound effects using Python's built-in `winsound`
module, which is available on Windows without installing anything extra.
Each function generates a tone at a specific frequency and duration to
create different sound effects for game events.

winsound.Beep(frequency, duration) plays a tone:
  - frequency: pitch in Hertz (Hz). Higher numbers = higher pitch.
  - duration: how long the sound lasts, in milliseconds.

We use this to create:
  - A satisfying "chomp" sound when eating regular food.
  - An exciting "power-up" sound when eating special food.
  - A sad "game over" sound when the snake crashes.
  - A cheerful "level up" sound when advancing to a new level.
"""

import winsound


# ==================================================================
# Sound effect functions
# ==================================================================

def eat_food():
    """Play a short, satisfying 'chomp' sound when eating regular food.

    Uses a medium-high pitch beep that lasts a very short time,
    giving a quick, pleasant feedback sound.
    """
    try:
        winsound.Beep(600, 80)   # 600 Hz for 80 milliseconds
    except Exception:
        # Silently ignore if sound fails (e.g., no audio device)
        pass


def eat_special_food():
    """Play an exciting 'power-up' sound when eating special food.

    Plays two quick beeps that go up in pitch, creating a
    rising 'power-up' effect that feels rewarding.
    """
    try:
        winsound.Beep(800, 60)   # First beep: 800 Hz for 60ms
        winsound.Beep(1200, 100) # Second beep: 1200 Hz for 100ms (higher pitch)
    except Exception:
        pass


def game_over():
    """Play a sad 'game over' sound when the snake crashes.

    Plays three beeps that go down in pitch, creating a
    descending 'game over' melody that feels like a loss.
    """
    try:
        winsound.Beep(400, 150)  # First beep: 400 Hz for 150ms
        winsound.Beep(300, 150)  # Second beep: 300 Hz for 150ms (lower)
        winsound.Beep(200, 300)  # Third beep: 200 Hz for 300ms (lowest, longest)
    except Exception:
        pass


def level_up():
    """Play a cheerful 'level up' sound when advancing to a new level.

    Plays three quick beeps that go up in pitch, creating a
    celebratory 'level up' fanfare.
    """
    try:
        winsound.Beep(500, 60)   # First beep: 500 Hz for 60ms
        winsound.Beep(700, 60)   # Second beep: 700 Hz for 60ms (higher)
        winsound.Beep(900, 120)  # Third beep: 900 Hz for 120ms (highest, longer)
    except Exception:
        pass
