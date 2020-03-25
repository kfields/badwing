import arcade


# Size of the window
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'BadWing'

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

# Grid-size
SPRITE_SIZE = 64

# How close we get to the edge before scrolling
VIEWPORT_MARGIN = 100

# Constants used to scale our sprites from their original size
SPRITE_SCALING = 0.5
CHARACTER_SCALING = 1
TILE_SCALING = 1
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# Kinematic Constants
# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10
PLAYER_JUMP_SPEED = 25
K_GRAVITY = 1

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 100

# Debug
DEBUG_COLLISION = False

RAINBOW_COLORS = (
    arcade.color.ELECTRIC_CRIMSON,
    arcade.color.FLUORESCENT_ORANGE,
    arcade.color.ELECTRIC_YELLOW,
    arcade.color.ELECTRIC_GREEN,
    arcade.color.ELECTRIC_CYAN,
    arcade.color.MEDIUM_ELECTRIC_BLUE,
    arcade.color.ELECTRIC_INDIGO,
    arcade.color.ELECTRIC_PURPLE,
)
SPARK_TEXTURES = [arcade.make_circle_texture(8, clr) for clr in RAINBOW_COLORS]
SPARK_PAIRS = [
    [SPARK_TEXTURES[0], SPARK_TEXTURES[3]],
    [SPARK_TEXTURES[1], SPARK_TEXTURES[5]],
    [SPARK_TEXTURES[7], SPARK_TEXTURES[2]],
]
ROCKET_SMOKE_TEXTURE = arcade.make_soft_circle_texture(15, arcade.color.GRAY)
PUFF_TEXTURE = arcade.make_soft_circle_texture(80, (40, 40, 40))
FLASH_TEXTURE = arcade.make_soft_circle_texture(70, (128, 128, 90))
CLOUD_TEXTURES = [
    arcade.make_soft_circle_texture(50, arcade.color.WHITE),
    arcade.make_soft_circle_texture(50, arcade.color.LIGHT_GRAY),
    arcade.make_soft_circle_texture(50, arcade.color.LIGHT_BLUE),
]
STAR_TEXTURES = [
    arcade.make_soft_circle_texture(8, arcade.color.WHITE),
    arcade.make_soft_circle_texture(8, arcade.color.PASTEL_YELLOW),
]
SPINNER_HEIGHT = 75