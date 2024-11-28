# Size of the window
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'BadWing'

# Debug
DEBUG_COLLISION = False

# Default friction used for sprites, unless otherwise specified
DEFAULT_FRICTION = 0.2

# Default mass used for sprites
DEFAULT_MASS = 1

# Gravity
GRAVITY = (0.0, -900.0)
#GRAVITY = (0.0, 0.0)

# Player forces
PLAYER_MOVE_FORCE = 700
PLAYER_JUMP_IMPULSE = 600
PLAYER_PUNCH_IMPULSE = 600

# Kinematic Constants
# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 500
PLAYER_JUMP_SPEED = 750

# Physics Types

PT_STATIC = 0
PT_KINEMATIC = 1
PT_DYNAMIC = 2
PT_GROUP = 3

# Grid-size
SPRITE_SIZE = 128

# How close we get to the edge before scrolling
VIEWPORT_MARGIN = 100

# Constants used to scale our sprites from their original size
SPRITE_SCALING = 0.5
CHARACTER_SCALING = 1

TILE_WIDTH = 128
TILE_SCALING = 1
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 100
