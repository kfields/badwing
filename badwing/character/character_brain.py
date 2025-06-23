from loguru import logger

from crunge.engine.loader.sprite.xml_sprite_atlas_loader import XmlSpriteAtlasLoader
from crunge.engine.builder.sprite import CollidableSpriteBuilder
from crunge.engine.d2.sprite import SpriteAnimator, SpriteAnimationFrame, SpriteAnimation

from badwing.brain import Brain

# Constants used to track if the player character is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

class Command:
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    PUNCH = "punch"

class CharacterBrain(Brain):
    def __init__(self):
        super().__init__()

        self.animator: SpriteAnimator = None
        # Default to face-right
        self.character_face_direction = RIGHT_FACING

    def _create(self):
        super()._create()
        self.animator = SpriteAnimator(self.node)
        atlas = XmlSpriteAtlasLoader(sprite_builder=CollidableSpriteBuilder()).load(
            ":resources:/characters/male_adventurer/sheet.xml"
        )
        self.create_idle_animations(atlas, self.animator)
        self.create_climb_animations(atlas, self.animator)
        self.create_jump_animations(atlas, self.animator)
        self.create_fall_animations(atlas, self.animator)
        self.create_walk_animations(atlas, self.animator)

    def create_idle_animations(self, atlas: XmlSpriteAtlasLoader, animator: SpriteAnimator):
        idle = SpriteAnimation("idle")
        frame = SpriteAnimationFrame(atlas.get(f"idle"))
        idle.add_frame(frame)

        animator.add_animation(idle)

    def create_climb_animations(self, atlas: XmlSpriteAtlasLoader, animator: SpriteAnimator):
        climb = SpriteAnimation("climb")
        for i in range(0, 2):
            frame = SpriteAnimationFrame(atlas.get(f"climb{i}"))
            climb.add_frame(frame)

        animator.add_animation(climb)

    def create_jump_animations(self, atlas: XmlSpriteAtlasLoader, animator: SpriteAnimator):
        jump = SpriteAnimation("jump")
        frame = SpriteAnimationFrame(atlas.get(f"jump"))
        jump.add_frame(frame)

        animator.add_animation(jump)

    def create_fall_animations(self, atlas: XmlSpriteAtlasLoader, animator: SpriteAnimator):
        fall = SpriteAnimation("fall")
        frame = SpriteAnimationFrame(atlas.get(f"fall"))
        fall.add_frame(frame)

        animator.add_animation(fall)
        
    def create_walk_animations(self, atlas: XmlSpriteAtlasLoader, animator: SpriteAnimator):
        walk_right = SpriteAnimation("walkRight")
        for i in range(0, 8):
            frame = SpriteAnimationFrame(atlas.get(f"walk{i}"))
            walk_right.add_frame(frame)

        animator.add_animation(walk_right)

        walk_left = walk_right.mirror("walkLeft", horizontal=True)

        animator.add_animation(walk_left)

    def update(self, delta_time: float = 1/60):
        super().update(delta_time)
        node = self.node
        velocity = node.body.velocity
        vel_x = int(velocity[0])
        vel_y = int(velocity[1])

        #TODO: update node velocity from body
        '''
        velocity = self.node.velocity
        vel_x = velocity.x
        vel_y = velocity.y
        '''

        # Figure out if we need to flip face left or right
        if vel_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif vel_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        '''
        # Climbing animation
        if node.laddered:
            #logger.debug("On ladder")
            node.climbing = True
        if not node.laddered and node.climbing:
            node.climbing = False
        '''

        '''
        if node.climbing and abs(vel_y) > 1:
            self.cur_sprite += 1
            if self.cur_sprite > 7:
                self.cur_sprite = 0
        if node.climbing:
            self.sprite = self.climbing_sprites[self.cur_sprite // 4]
            return
        '''

        # Climbing animation
        if node.climbing :
            self.animator.play("climb")
            if abs(vel_y) < 1:
                return
        # Jumping animation
        elif vel_y > 0 and not node.climbing or node.mounted or node.jumping:
            self.animator.play("jump")
        elif vel_y < 0 and not node.grounded and not node.climbing:
            self.animator.play("fall")
        # Idle animation
        elif vel_x == 0:
            self.animator.play("idle")
        else:
            # Walking animation
            self.animator.play("walkRight" if self.character_face_direction == RIGHT_FACING else "walkLeft")

        self.animator.update(delta_time)
