import math
import glm
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.autogeometry import convex_decomposition, to_convex_hull

import arcade
from arcade import check_for_collision_with_list
from arcade import check_for_collision

from badwing.constants import *
import badwing.app

from badwing.util import debounce
from badwing.model import Model, DynamicModel, KinematicModel
from badwing.physics.util import check_grounding
from badwing.character import CharacterAvatar

CHARACTER_SCALING = 1

UPDATES_PER_FRAME = 7

# Constants used to track if the player character is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

PLAYER_MASS = 1

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]

class PcSprite(arcade.Sprite):
    def __init__(self, position):
        super().__init__(center_x=position[0], center_y=position[1])

        # Animation timing
        self.time = 1
        self.update_time = 0
        #self.rate = 1/60
        self.rate = 1/30

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        # main_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"
        # main_path = ":resources:images/animated_characters/female_person/femalePerson"
        # main_path = ":resources:images/animated_characters/male_person/malePerson"
        main_path = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        # main_path = ":resources:images/animated_characters/zombie/zombie"
        # main_path = ":resources:images/animated_characters/robot/robot"

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
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        self.set_hit_box(self.texture.hit_box_points)

    def update_animation(self, delta_time: float = 1/60):
        self.time += delta_time
        if self.update_time > self.time:
            return
        self.update_time = self.time + self.rate

        velocity = self.model.body.velocity
        vel_x = velocity[0]
        vel_y = velocity[1]
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

class PlayerCharacter(KinematicModel):
    def __init__(self, sprite, position=(0,0)):
        super().__init__(sprite)

    def on_mount(self, position):
        super().on_mount()
        #print('on_mount')
        width = self.sprite.texture.width * TILE_SCALING
        height = self.sprite.texture.height * TILE_SCALING
        badwing.app.physics_engine.space.remove(self.body, self.shapes)
        self.body = body = self.create_dynamic_body(self.sprite, position)
        transform = pymunk.Transform(ty=height/2)
        self.create_hull_shapes(self.sprite, self.body, position, collision_type=PT_DYNAMIC, transform=transform)
        badwing.app.physics_engine.space.add(self.body, self.shapes)

    def on_dismount(self, position):
        super().on_dismount()
        #print('on_dismount')
        width = self.sprite.texture.width * TILE_SCALING
        height = self.sprite.texture.height * TILE_SCALING
        badwing.app.physics_engine.space.remove(self.body, self.shapes)
        self.body = body = self.create_kinematic_body(self.sprite, position)
        self.create_hull_shapes(self.sprite, self.body, position)
        badwing.app.physics_engine.space.add(self.body, self.shapes)
        badwing.app.scene.pop_pc()

    @classmethod
    def create(self, position=(192, 292)):
        sprite = PcSprite(position)
        return PlayerCharacter(sprite, position)

    def control(self):
        return PcAvatar(self)

    def on_add(self, layer):
        super().on_add(layer)
        layer.add_sprite(self.sprite)

    def create_kinematic_body(self, sprite, position=(0,0)):
        width = sprite.texture.width * TILE_SCALING
        height = sprite.texture.height * TILE_SCALING


        mass = PLAYER_MASS
        moment = pymunk.moment_for_box(mass, (width, height))
        #moment = pymunk.moment_for_poly(mass, points)
        body = pymunk.Body(mass, moment, body_type=pymunk.Body.KINEMATIC)
        body.position = position
        body.model = self
        return body

    def create_dynamic_body(self, sprite, position=(0,0)):
        width = sprite.texture.width * TILE_SCALING
        height = sprite.texture.height * TILE_SCALING


        mass = PLAYER_MASS
        moment = pymunk.moment_for_box(mass, (width, height))
        body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
        body.model = self

        pc_pos = Vec2d(position)
        self.body_offset = body_offset = Vec2d(0, -height/2)
        body.position = pc_pos + body_offset
        return body
    
    def create_poly_shapes(self, sprite, body, position, collision_type=PT_KINEMATIC, transform=None):
        self.shapes = []
        sprite.position = position
        center = Vec2d(position)
        points = sprite.points
        polys = convex_decomposition(sprite.points, 0)
        for poly in polys:
            points = [i - center for i in poly ]
            shape = pymunk.Poly(body, points, transform)
            shape.friction = 10
            shape.elasticity = 0.2
            shape.collision_type = collision_type
            self.shapes.append(shape)

    def create_hull_shapes(self, sprite, body, position, collision_type=PT_KINEMATIC, transform=None):
        self.shapes = []
        sprite.position = position
        center = Vec2d(position)
        points = sprite.points
        poly = to_convex_hull(sprite.points, .01)
        points = [i - center for i in poly ]
        shape = pymunk.Poly(body, points, transform)
        shape.friction = 10
        shape.elasticity = 0.2
        shape.collision_type = collision_type
        self.shapes.append(shape)
    
    # Hack in sprite transform here for now.  Move up the hierarchy later
    def update_sprite(self, delta_time=1/60):
        if not self.mounted:
            super().update_sprite(delta_time)
            return

        body_pos = self.body.position
        angle = self.body.angle
        model = glm.mat4()
        model = glm.rotate(model, angle, glm.vec3(0, 0, 1))
        rel_pos = model * glm.vec4(0, 64, 0, 1)
        pos = rel_pos + glm.vec4(body_pos[0], body_pos[1], 0, 1) 
        self.sprite.position = (pos[0], pos[1])
        self.sprite.angle = math.degrees(angle)

class PcAvatar(CharacterAvatar):
    def __init__(self, pc):
        super().__init__(pc)
        self.physics_engine = badwing.app.physics_engine
        self.pc = pc
        self.pc_sprite = pc.sprite
        self.force = (0, 0)
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        #
        self.character_layer = badwing.app.scene.character_layer
        self.platforms = badwing.app.scene.ground_layer.sprites
        self.ladders = badwing.app.scene.ladder_layer.sprites

        self.jumps_since_ground = 0
        self.allowed_jumps = 1
        self.allow_multi_jump = False

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

    def mount(self):
        hit_list = arcade.check_for_collision_with_list(self.pc_sprite, self.character_layer.sprites)
        for sprite in hit_list:
            model = sprite.model
            if isinstance(model, badwing.characters.Chassis):
                mount = model.parent
                mount.mount(self.pc)
                badwing.app.scene.push_pc(mount)

    def is_on_ladder(self):
        laddered = self.model.laddered
        if self.ladders:
            hit_list = check_for_collision_with_list(self.pc_sprite, self.ladders)
            if len(hit_list) > 0:
                self.model.laddered = laddered = True
            else:
                self.model.laddered = laddered = False
        return laddered

    def can_jump(self, y_distance=5) -> bool:
        # Move down to see if we are on a platform
        self.pc_sprite.center_y -= y_distance

        # Check for wall hit
        hit_list = check_for_collision_with_list(self.pc_sprite, self.platforms)

        self.pc_sprite.center_y += y_distance

        if len(hit_list) > 0:
            self.jumps_since_ground = 0

        if len(hit_list) > 0 or self.allow_multi_jump and self.jumps_since_ground < self.allowed_jumps:
            return True
        else:
            return False

    def enable_multi_jump(self, allowed_jumps: int):
        self.allowed_jumps = allowed_jumps
        self.allow_multi_jump = True

    def disable_multi_jump(self):
        self.allow_multi_jump = False
        self.allowed_jumps = 1
        self.jumps_since_ground = 0

    def jump(self, velocity: int):
        self.pc_sprite.change_y = velocity
        self.increment_jump_counter()

    def increment_jump_counter(self):
        if self.allow_multi_jump:
            self.jumps_since_ground += 1

    def update(self, delta_time=1/60):
        super().update(delta_time)

    def process_keychange(self):
        delta_x, delta_y = 0, 0
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.is_on_ladder():
                delta_y = PLAYER_MOVEMENT_SPEED
            elif self.pc.grounded and not self.jump_needs_reset:
                delta_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.is_on_ladder():
                delta_y = -PLAYER_MOVEMENT_SPEED
            else:
                self.mount()

        # Process up/down when on a ladder and no movement
        if self.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                delta_y = 0
            elif self.up_pressed and self.down_pressed:
                delta_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            delta_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            delta_x = -PLAYER_MOVEMENT_SPEED
        else:
            #self.pc_sprite.change_x = 0
            delta_x = 0

        self.pc.body.velocity = (delta_x, delta_y)


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.SPACE:
            self.pc.punching = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.SPACE:
            self.pc.punching = False

        self.process_keychange()
