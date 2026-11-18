"""
gui.py — Drawing and keyboard event handlers for SnakeGH.

This module owns the Tkinter window, canvas, and labels.  It knows how
to paint the snake, food, grid, and messages on the screen, and how to
translate key presses into direction changes.

It does NOT own the game rules — those live in logic.py and game.py.
"""

import tkinter as tk

from constants import (
    CELL, WIDTH, HEIGHT,
    BG_COLOUR, CANVAS_COLOUR, GRID_COLOUR,
    SNAKE_HEAD, SNAKE_BODY, FOOD_COLOUR, SPECIAL_FOOD,
    TITLE_COLOUR, TEXT_COLOUR, SUB_COLOUR, HINT_COLOUR,
    KEYS,
)

import eyes
import special_food


# ==================================================================
# Placeholder references — filled in by SnakeGH.py after Tk starts
# ==================================================================

canvas      = None            # tk.Canvas — the game board
score_label = None            # tk.Label — shows score / level / best
root        = None            # tk.Tk — the main window (for after())


# ------------------------------------------------------------------
# Grid drawing
# ------------------------------------------------------------------

def draw_grid():
    """Draw faint grid lines once, at the start.

    The grid is drawn only once because it never changes.  Every tick
    we only redraw the snake and food on top of it.
    """
    # Vertical lines.
    for x in range(0, WIDTH, CELL):
        canvas.create_line(x, 0, x, HEIGHT, fill=GRID_COLOUR)
    # Horizontal lines.
    for y in range(0, HEIGHT, CELL):
        canvas.create_line(0, y, WIDTH, y, fill=GRID_COLOUR)


# ------------------------------------------------------------------
# Score label update
# ------------------------------------------------------------------

def update_labels():
    """Refresh the score / level / best label with current game state."""
    from game import score, level, high_score
    score_label.config(
        text=f"Score: {score}   Level: {level}   Best: {high_score}"
    )


# ------------------------------------------------------------------
# Main draw function (called every tick)
# ------------------------------------------------------------------

def draw():
    """Clear the old snake and food, then draw them in their new places.

    This is the function the game loop calls after every tick to update
    the visual state of the board.  It also draws the special food (if
    present) and the snake's eyes on the head.
    """
    from game import snake, food, direction

    # Remove only the snake and food shapes (tags="piece"), plus any
    # overlay messages (tags="message").  The grid lines stay.
    canvas.delete("piece", "message")

    # Draw the regular food as a small red circle.
    fx, fy = food
    canvas.create_oval(
        fx * CELL + 4, fy * CELL + 4,
        fx * CELL + CELL - 4, fy * CELL + CELL - 4,
        fill=FOOD_COLOUR, outline="", tags="piece"
    )

    # Draw the special food as a gold star-like shape (if it exists and hasn't expired).
    # We check is_expired() here too, in case it expired between ticks.
    if not special_food.is_expired():
        sp_pos = special_food.special_food
        if sp_pos is not None:
            sx, sy = sp_pos
            # Draw a gold circle with a white outline for the special food.
            canvas.create_oval(
                sx * CELL + 2, sy * CELL + 2,
                sx * CELL + CELL - 2, sy * CELL + CELL - 2,
                fill=SPECIAL_FOOD, outline="#ffffff", outlinewidth=1, tags="piece"
            )
            # Draw a small "★" star symbol in the center to make it look special.
            canvas.create_text(
                sx * CELL + CELL // 2, sy * CELL + CELL // 2,
                text="★", fill="#000000", font=("Segoe UI", 10, "bold"), tags="piece"
            )

    # Draw each snake segment as a green rectangle.
    # The head (index 0) is a darker green; the body is lighter.
    for index, (x, y) in enumerate(snake):
        colour = SNAKE_HEAD if index == 0 else SNAKE_BODY
        canvas.create_rectangle(
            x * CELL + 1, y * CELL + 1,
            x * CELL + CELL - 1, y * CELL + CELL - 1,
            fill=colour, outline="", tags="piece"
        )

    # Draw eyes on the snake's head (the first segment).
    if snake:
        head_x, head_y = snake[0]
        eyes.draw_eyes(canvas, head_x, head_y, direction)

    # Update the score label.
    update_labels()


# ------------------------------------------------------------------
# Overlay messages (start screen, game over, pause)
# ------------------------------------------------------------------

def show_message(title, subtitle):
    """Write a big centred message on the canvas.

    Parameters
    ----------
    title : str
        Large text (e.g. "Game Over!").
    subtitle : str
        Smaller text below it (e.g. "Space to restart").
    """
    canvas.create_text(
        WIDTH // 2, HEIGHT // 2 - 20,
        text=title, fill=TEXT_COLOUR,
        font=("Segoe UI", 28, "bold"), tags="message"
    )
    canvas.create_text(
        WIDTH // 2, HEIGHT // 2 + 20,
        text=subtitle, fill=SUB_COLOUR,
        font=("Segoe UI", 12), tags="message"
    )


# ------------------------------------------------------------------
# Keyboard event handler
# ------------------------------------------------------------------

def on_key(event):
    """Handle every key press.

    Maps arrow keys and WASD to direction changes, Space to start /
    restart, and P to pause / resume.

    Parameters
    ----------
    event : tk.Event
        The key-press event.
    """
    from game import running, change_direction, start_game, toggle_pause

    key = event.keysym.lower()

    # Space — start a new game or restart after game over.
    if key == "space":
        if not running:
            start_game(root)
        return

    # P — pause / resume.
    if key == "p":
        toggle_pause(root)
        return

    # Arrow keys / WASD — change direction.
    if key in KEYS:
        change_direction(KEYS[key])


# ------------------------------------------------------------------
# Build the window
# ------------------------------------------------------------------

def build_window():
    """Create the Tkinter window, canvas, labels, and bind events.

    Returns the root window so the caller can start the main loop.
    """
    global root, canvas, score_label

    # --- Main window ---
    root = tk.Tk()
    root.title("SnakeGH - Classic Arcade Game")
    root.resizable(False, False)
    root.configure(bg=BG_COLOUR)

    # --- Title ---
    tk.Label(
        root, text="SnakeGH",
        font=("Segoe UI", 22, "bold"),
        fg=TITLE_COLOUR, bg=BG_COLOUR
    ).pack(pady=(10, 0))

    # --- Score / Level / Best ---
    score_label = tk.Label(
        root,
        text="Score: 0   Level: 1   Best: 0",
        font=("Consolas", 13, "bold"),
        fg=TEXT_COLOUR, bg=BG_COLOUR
    )
    score_label.pack(pady=(0, 8))

    # --- Game canvas ---
    canvas = tk.Canvas(
        root, width=WIDTH, height=HEIGHT,
        bg=CANVAS_COLOUR, highlightthickness=0
    )
    canvas.pack(padx=15)

    # --- Control hints ---
    tk.Label(
        root,
        text="Arrows / W A S D = move     P = pause     Space = start",
        fg=HINT_COLOUR, bg=BG_COLOUR
    ).pack(pady=8)

    # --- Draw the grid (once) ---
    draw_grid()

    # --- Bind keyboard ---
    root.bind("<Key>", on_key)

    return root
