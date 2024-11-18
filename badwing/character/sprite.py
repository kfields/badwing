from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader
from crunge.engine.d2.sprite import Sprite, SpriteVu

CHARACTER_SCALING = 1

UPDATES_PER_FRAME = 7

# Constants used to track if the player character is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        #arcade.load_texture(filename),
        ImageTextureLoader().load(filename),
        #arcade.load_texture(filename, flipped_horizontally=True)
        #arcade.load_texture(filename).flip_horizontally()
        ImageTextureLoader().load(filename)
    ]

class CharacterSprite(SpriteVu):
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
        self.cur_texture = 0
        #self.scale = CHARACTER_SCALING

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        # --- Load Textures ---

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        self.climbing_textures = []
        #texture = arcade.load_texture(f"{main_path}_climb0.png")
        texture = ImageTextureLoader().load(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        #texture = arcade.load_texture(f"{main_path}_climb1.png")
        texture = ImageTextureLoader().load(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        #self.set_hit_box(self.texture.hit_box_points)
        #self.hit_box = arcade.hitbox.RotatableHitBox(self.texture.hit_box_points)
        self.sprite = Sprite(self.texture)

    def update_animation(self, delta_time: float = 1/60):
        self.time += delta_time
        if self.update_time > self.time:
            return
        self.update_time = self.time + self.rate

        velocity = self.model.body.velocity
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
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return

        # Jumping animation
        if vel_y > 0 and not self.is_on_ladder or self.model.mounted:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif vel_y < 0 and not self.model.grounded and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if vel_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
