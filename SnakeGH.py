"""
SnakeGH - A Classic Arcade Game
Lab 2 - Python (Level 200)
Name: <Anyawoe Sheena Ama> | Index No: <2526403292>

This is the MAIN ENTRY POINT for the game.  When you run this file
(`python SnakeGH.py`) it:

  1. Imports all the other modules.
  2. Builds the window and canvas (gui.py).
  3. Wires the GUI callbacks into the game loop (game.py).
  4. Shows the start-screen message.
  5. Starts the Tkinter event loop so the window stays open.

The actual game logic lives in the other files — this file just connects
everything together.
"""

# ------------------------------------------------------------------
# Import our modules
# ------------------------------------------------------------------

import gui
import game
import sounds
import special_food
import eyes
from constants import WIDTH, HEIGHT


# ------------------------------------------------------------------
# Wire the GUI callbacks into game.py
# ------------------------------------------------------------------
#
# game.py needs to call back into gui.py to draw the board and show
# messages, but we don't want game.py to import gui.py directly
# (that would create a circular import).  Instead we set the callback
# references here, after both modules are loaded.

game.gui_draw = gui.draw
game.gui_show_message = gui.show_message
game.root = gui.root          # will be set by build_window() below


# ------------------------------------------------------------------
# Build the window
# ------------------------------------------------------------------

root = gui.build_window()

# Now that build_window() has created gui.root, update game.root.
game.root = gui.root


# ------------------------------------------------------------------
# Initialise game state and show the start screen
# ------------------------------------------------------------------

game.init_game()
gui.draw()
gui.show_message(
    "SnakeGH",
    "Press Space to start"
)


# ------------------------------------------------------------------
# Start the Tkinter event loop
# ------------------------------------------------------------------
#
# This blocks here and keeps the window alive.  It processes key presses
# and schedules the game-loop ticks via root.after().

root.mainloop()