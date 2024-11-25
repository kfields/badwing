from loguru import logger

from crunge.engine.math import Rect2i
#from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.builder.sprite import CollidableSpriteBuilder

from badwing.brain import Brain

CHARACTER_SCALING = 1

UPDATES_PER_FRAME = 7

# Constants used to track if the player character is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

def load_sprite_pair(filename, sprite_loader: SpriteLoader):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        sprite_loader.load(filename),
        #arcade.load_texture(filename).flip_horizontally()
        sprite_loader.load(filename) #TODO: flip horizontally
    ]

class CharacterBrain(Brain):
    def __init__(self, main_path = ":resources:/animated_characters/male_adventurer/character_maleAdventurer"):
        super().__init__()

        # Animation timing
        self.time = 1
        self.update_time = 0
        #self.rate = 1/60
        self.rate = 1/30

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_sprite = 0
        #self.scale = CHARACTER_SCALING

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        '''
        # --- Load Sprites ---
        sprite_loader = SpriteLoader(sprite_builder = CollidableSpriteBuilder())
        # Load textures for idle standing
        self.idle_sprite_pair = load_sprite_pair(f"{main_path}_idle.png", sprite_loader)
        self.jump_sprite_pair = load_sprite_pair(f"{main_path}_jump.png", sprite_loader)
        self.fall_sprite_pair = load_sprite_pair(f"{main_path}_fall.png", sprite_loader)

        # Load textures for walking
        self.walk_sprites = []
        for i in range(8):
            sprite = load_sprite_pair(f"{main_path}_walk{i}.png", sprite_loader)
            self.walk_sprites.append(sprite)

        # Load textures for climbing
        self.climbing_sprites = []
        #texture = arcade.load_texture(f"{main_path}_climb0.png")
        sprite = sprite_loader.load(f"{main_path}_climb0.png")
        self.climbing_sprites.append(sprite)
        #texture = arcade.load_texture(f"{main_path}_climb1.png")
        sprite = sprite_loader.load(f"{main_path}_climb1.png")
        self.climbing_sprites.append(sprite)

        # Set the initial texture
        self.sprite = self.idle_sprite_pair[self.character_face_direction]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        #self.set_hit_box(self.texture.hit_box_points)
        #self.hit_box = arcade.hitbox.RotatableHitBox(self.texture.hit_box_points)
        #self.sprite = Sprite(self.texture)
        #sprite_builder = CollidableSpriteBuilder()
        #size = self.texture.size
        #rect = Rect2i(0, 0, size.x, size.y)
        #self.sprite = sprite_builder.build(self.texture, rect)
        '''

    def _create(self):
        super()._create()
        main_path = ":resources:/animated_characters/male_adventurer/character_maleAdventurer"
        sprite_loader = SpriteLoader(sprite_builder = CollidableSpriteBuilder())
        # Load textures for idle standing
        self.idle_sprite_pair = load_sprite_pair(f"{main_path}_idle.png", sprite_loader)
        self.jump_sprite_pair = load_sprite_pair(f"{main_path}_jump.png", sprite_loader)
        self.fall_sprite_pair = load_sprite_pair(f"{main_path}_fall.png", sprite_loader)

        # Load textures for walking
        self.walk_sprites = []
        for i in range(8):
            sprite = load_sprite_pair(f"{main_path}_walk{i}.png", sprite_loader)
            self.walk_sprites.append(sprite)

        # Load textures for climbing
        self.climbing_sprites = []
        #texture = arcade.load_texture(f"{main_path}_climb0.png")
        sprite = sprite_loader.load(f"{main_path}_climb0.png")
        self.climbing_sprites.append(sprite)
        #texture = arcade.load_texture(f"{main_path}_climb1.png")
        sprite = sprite_loader.load(f"{main_path}_climb1.png")
        self.climbing_sprites.append(sprite)

        # Set the initial texture
        self.sprite = self.idle_sprite_pair[self.character_face_direction]

    def update(self, delta_time: float = 1/60):
        super().update(delta_time)
        self.time += delta_time
        if self.update_time > self.time:
            return
        self.update_time = self.time + self.rate

        velocity = self.node.body.velocity
        vel_x = int(velocity[0])
        vel_y = int(velocity[1])
        #print(vel_x, vel_y)
        # Figure out if we need to flip face left or right
        if vel_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif vel_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Climbing animation
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(vel_y) > 1:
            self.cur_sprite += 1
            if self.cur_sprite > 7:
                self.cur_sprite = 0
        if self.climbing:
            self.sprite = self.climbing_sprites[self.cur_sprite // 4]
            return

        # Jumping animation
        if vel_y > 0 and not self.is_on_ladder or self.node.mounted:
            self.sprite = self.jump_sprite_pair[self.character_face_direction]
            return
        elif vel_y < 0 and not self.node.grounded and not self.is_on_ladder:
            self.sprite = self.fall_sprite_pair[self.character_face_direction]
            return

        # Idle animation
        if vel_x == 0:
            self.sprite = self.idle_sprite_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_sprite += 1
        if self.cur_sprite > 7:
            self.cur_sprite = 0
        self.sprite = self.walk_sprites[self.cur_sprite][self.character_face_direction]
