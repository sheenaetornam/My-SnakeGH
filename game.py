"""
game.py — Game state and game-loop for SnakeGH.

This module owns all the *mutable* game data: the snake body list, the
current direction, the score, the level, and whether the game is running
or paused.  It also contains the game-loop function that is called every
tick to move the snake, check for collisions, and handle eating food.

The game loop does NOT draw anything itself — it only updates the data.
After each tick it asks the GUI module to redraw.
"""

from logic import next_head, hits_wall, hits_self, random_food, level_for, speed_for
from high_score import load_high_score, save_high_score
from constants import OPPOSITE
import sounds
import special_food

# These are set by SnakeGH.py after the GUI is built.
gui_draw = None
gui_show_message = None
root = None


# ==================================================================
# Game-state variables (global so the GUI can read them)
# ==================================================================

snake           = []          # list of (x, y) tuples — index 0 is the head
direction       = "Right"     # current movement direction
next_direction  = "Right"     # direction queued by the player this tick
food            = (0, 0)      # current food position (x, y)
score           = 0           # current score
high_score      = 0           # best score loaded from disk
level           = 1           # current level
running         = False       # True while the game is actively running
paused          = False       # True when the player pressed Pause
loop_id         = None        # Tkinter after() handle so we can cancel it


# ------------------------------------------------------------------
# Initialisation
# ------------------------------------------------------------------

def init_game():
    """Reset all game-state variables to their starting values.

    Called once at program start and again every time the player begins
    a new game.
    """
    global snake, direction, next_direction, food, score, level
    global running, paused, loop_id, high_score

    # Load the persistent high score from disk.
    high_score = load_high_score()

    # Start with a 3-segment snake in the middle-left of the board.
    snake = [(5, 10), (4, 10), (3, 10)]
    direction = "Right"
    next_direction = "Right"

    # Place the first food on a random empty cell.
    food = random_food(snake)

    score = 0
    level = 1
    running = False
    paused = False
    loop_id = None

    # Reset the special food state.
    special_food.reset()


# ------------------------------------------------------------------
# Direction change (called by the GUI when a key is pressed)
# ------------------------------------------------------------------

def change_direction(new_dir):
    """Queue a new direction, preventing a 180° reversal.

    We store the request in *next_direction* instead of *direction* so
    that two quick key presses in one tick are both respected (a common
    bug in simple snake games is lost key presses).

    Parameters
    ----------
    new_dir : str
        The direction the player pressed ("Up", "Down", "Left", "Right").
    """
    global next_direction

    # The snake cannot reverse into itself.
    if OPPOSITE[new_dir] != direction:
        next_direction = new_dir


# ------------------------------------------------------------------
# Pause / unpause
# ------------------------------------------------------------------

def toggle_pause(root):
    """Toggle the pause state and (re)schedule the loop accordingly.

    Parameters
    ----------
    root : tk.Tk
        The main Tkinter window (needed for root.after).
    """
    global paused, loop_id

    if not running:
        return

    if paused:
        # Resume: schedule the next tick.
        paused = False
        loop_id = root.after(speed_for(level), _tick)
    else:
        # Pause: cancel the scheduled tick.
        paused = True
        if loop_id is not None:
            root.after_cancel(loop_id)
            loop_id = None


# ------------------------------------------------------------------
# Start a new game
# ------------------------------------------------------------------

def start_game(root):
    """Reset the board and start the game loop.

    Parameters
    ----------
    root : tk.Tk
        The main Tkinter window.
    """
    global snake, direction, next_direction, food, score, level
    global running, paused, loop_id

    # Cancel any existing loop first.
    if loop_id is not None:
        root.after_cancel(loop_id)
        loop_id = None

    # Reset state.
    snake = [(5, 10), (4, 10), (3, 10)]
    direction = "Right"
    next_direction = "Right"
    food = random_food(snake)
    score = 0
    level = 1
    running = True
    paused = False

    # Reset the special food state for the new game.
    special_food.reset()

    # Kick off the loop.
    loop_id = root.after(speed_for(level), _tick)


# ------------------------------------------------------------------
# The game loop (one tick)
# ------------------------------------------------------------------

def _tick():
    """One game tick: move the snake, check collisions, update score.

    This is the core loop called every few milliseconds.  It:
      1. Commits the queued direction.
      2. Computes the new head position.
      3. Checks for wall / self collisions → game over.
      4. Checks for food → grow and score.
      5. Checks for special food → bonus points and sound.
      6. Otherwise just move (add head, remove tail).
      7. Asks the GUI to redraw.
      8. Schedules the next tick.
    """
    global direction, loop_id, score, level, food, snake, running, paused

    # 1. Commit the direction queued this tick.
    direction = next_direction

    # 2. Compute where the head will be.
    head = next_head(snake[0], direction)

    # 3. Collision: wall or self → game over.
    if hits_wall(head) or hits_self(head, snake):
        _game_over()
        return

    # 4. Did the snake eat the regular food?
    if head == food:
        score += 1
        old_level = level
        level = level_for(score)
        # Grow: add the new head but do NOT remove the tail.
        snake.insert(0, head)
        # Place new food on a random empty cell.
        food = random_food(snake)

        # Play the eating sound.
        sounds.eat_food()

        # If we just leveled up, play the level-up sound.
        if level > old_level:
            sounds.level_up()

        # Try to spawn special food after eating regular food.
        special_food.maybe_spawn(snake)

    # 5. Did the snake eat the special food?
    elif special_food.at_position(head) and not special_food.is_expired():
        bonus = special_food.consume()
        score += bonus
        level = level_for(score)
        # Grow: add the new head but do NOT remove the tail.
        snake.insert(0, head)

        # Play the special food sound.
        sounds.eat_special_food()

    else:
        # Normal move: add head, remove tail.
        snake.insert(0, head)
        snake.pop()

    # 6. Ask the GUI to redraw the board.
    gui_draw()

    # 7. Schedule the next tick — only if still running and not paused.
    if running and not paused:
        loop_id = root.after(speed_for(level), _tick)


def _game_over():
    """Handle game-over: update high score and show the end screen."""
    global score, high_score, running

    running = False

    # Play the game-over sound.
    sounds.game_over()

    # Check for a new high score.
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    # Show the game-over message on the canvas.
    gui_show_message("Game Over!", f"Score: {score}   Best: {high_score}   Space to restart")
