"""
eyes.py — Draw eyes on the snake's head for SnakeGH.

This module draws two small eyes on the snake's head so it looks like
a real snake with a face. The eyes are positioned differently depending
on which direction the snake is facing, so the snake always appears to
be looking where it's going.

How it works:
  - Each eye is drawn as a white circle with a black pupil (smaller circle).
  - The eye positions are calculated based on the head's cell position
    and the current direction.
  - For left/right directions, the eyes are placed side by side on the
    front of the head.
  - For up/down directions, the eyes are placed one above the other on
    the front of the head.

The draw_eyes() function is called from gui.py after the head rectangle
is drawn, so the eyes appear on top of the head.
"""

from constants import CELL


# ==================================================================
# Eye drawing constants
# ==================================================================

EYE_WHITE = "#ffffff"      # White colour for the outer part of the eye.
EYE_PUPIL = "#000000"      # Black colour for the pupil (center of the eye).
EYE_RADIUS = 3             # Radius of the white eye circle, in pixels.
PUPIL_RADIUS = 1           # Radius of the black pupil, in pixels.


# ------------------------------------------------------------------
# Draw eyes on the canvas
# ------------------------------------------------------------------

def draw_eyes(canvas, head_x, head_y, direction):
    """Draw two eyes on the snake's head.

    The eyes are positioned based on the current direction so the snake
    appears to be looking forward.

    Parameters
    ----------
    canvas : tk.Canvas
        The Tkinter canvas to draw on.
    head_x : int
        The x-coordinate (in cells) of the snake's head.
    head_y : int
        The y-coordinate (in cells) of the snake's head.
    direction : str
        The current direction: "Up", "Down", "Left", or "Right".
    """
    # Convert cell coordinates to pixel coordinates.
    px = head_x * CELL
    py = head_y * CELL

    # Calculate the two eye positions based on direction.
    if direction == "Right":
        # Eyes on the right side of the head, side by side.
        eye1 = (px + CELL - 7, py + 6)
        eye2 = (px + CELL - 7, py + CELL - 6)
    elif direction == "Left":
        # Eyes on the left side of the head, side by side.
        eye1 = (px + 7, py + 6)
        eye2 = (px + 7, py + CELL - 6)
    elif direction == "Up":
        # Eyes on the top side of the head, one above the other.
        eye1 = (px + 6, py + 7)
        eye2 = (px + CELL - 6, py + 7)
    elif direction == "Down":
        # Eyes on the bottom side of the head, one above the other.
        eye1 = (px + 6, py + CELL - 7)
        eye2 = (px + CELL - 6, py + CELL - 7)
    else:
        # Fallback: eyes in the center (shouldn't happen).
        eye1 = (px + 6, py + 6)
        eye2 = (px + CELL - 6, py + CELL - 6)

    # Draw each eye: white outer circle + black pupil.
    for ex, ey in (eye1, eye2):
        # White outer circle.
        canvas.create_oval(
            ex - EYE_RADIUS, ey - EYE_RADIUS,
            ex + EYE_RADIUS, ey + EYE_RADIUS,
            fill=EYE_WHITE, outline="", tags="piece"
        )
        # Black pupil (smaller circle in the center).
        canvas.create_oval(
            ex - PUPIL_RADIUS, ey - PUPIL_RADIUS,
            ex + PUPIL_RADIUS, ey + PUPIL_RADIUS,
            fill=EYE_PUPIL, outline="", tags="piece"
        )
