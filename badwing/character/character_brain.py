from loguru import logger

import glm

from crunge.engine.loader.sprite.xml_sprite_atlas_loader import XmlSpriteAtlasLoader
from crunge.engine.builder.sprite import CollidableSpriteBuilder
from crunge.engine.d2.sprite import SpriteAnimator, SpriteAnimationFrame, SpriteAnimation
from crunge.engine.resource.sprite import SpriteAtlas

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
    def __init__(self, atlas: SpriteAtlas):
        super().__init__()
        self.atlas = atlas
        self.animator: SpriteAnimator = None
        # Default to face-right
        self.character_face_direction = RIGHT_FACING

    def _create(self):
        super()._create()
        self.animator = SpriteAnimator(self.node)
        self.create_idle_animations(self.atlas, self.animator)
        self.create_climb_animations(self.atlas, self.animator)
        self.create_jump_animations(self.atlas, self.animator)
        self.create_fall_animations(self.atlas, self.animator)
        self.create_walk_animations(self.atlas, self.animator)

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
        jump_right = SpriteAnimation("jumpRight")
        frame = SpriteAnimationFrame(atlas.get(f"jump"))
        jump_right.add_frame(frame)
        animator.add_animation(jump_right)

        jump_left = jump_right.mirror("jumpLeft", horizontal=True)
        animator.add_animation(jump_left)

    def create_fall_animations(self, atlas: XmlSpriteAtlasLoader, animator: SpriteAnimator):
        fall_right = SpriteAnimation("fallRight")
        frame = SpriteAnimationFrame(atlas.get(f"fall"))
        fall_right.add_frame(frame)
        animator.add_animation(fall_right)

        fall_left = fall_right.mirror("fallLeft", horizontal=True)
        animator.add_animation(fall_left)
        
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
        #TODO: update node velocity from body and get from node
        velocity = glm.vec2(node.body.velocity)

        # Figure out if we need to flip face left or right
        if velocity.x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif velocity.x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING


        # Climbing animation
        if node.climbing :
            self.animator.play("climb")
            if abs(velocity.y) < 1:
                return
        # Jumping animation
        elif velocity.y > 0 and not node.climbing or node.mounted or node.jumping:
            self.animator.play("jumpRight" if self.character_face_direction == RIGHT_FACING else "jumpLeft")
        elif velocity.y < 0 and not node.grounded and not node.climbing:
            self.animator.play("fallRight" if self.character_face_direction == RIGHT_FACING else "fallLeft")
        # Idle animation
        elif velocity.x == 0:
            self.animator.play("idle")
        else:
            # Walking animation
            self.animator.play("walkRight" if self.character_face_direction == RIGHT_FACING else "walkLeft")

        self.animator.update(delta_time)
