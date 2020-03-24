import random

import arcade

from badwing.constants import *
from badwing.layer import Layer
from badwing.particle import AnimatedAlphaParticle

class EmitterLayer(Layer):
    def __init__(self, level, name):
        super().__init__(level, name)
        self.emitters = []

    def setup(self):
        super().setup()

    def draw(self):
        for e in self.emitters:
            e.draw()

    def update(self, delta_time):
        # prevent list from being mutated (often by callbacks) while iterating over it
        emitters_to_update = self.emitters.copy()
        # update
        for e in emitters_to_update:
            e.update()
        # remove emitters that can be reaped
        to_del = [e for e in emitters_to_update if e.can_reap()]
        for e in to_del:
            self.emitters.remove(e)

    def make_sparks(self, position=(192,192)):
        spark_texture = random.choice(SPARK_TEXTURES)
        sparks = arcade.Emitter(
            center_xy=position,
            emit_controller=arcade.EmitBurst(random.randint(30, 40)),
            particle_factory=lambda emitter: AnimatedAlphaParticle(
                filename_or_texture=spark_texture,
                change_xy=arcade.rand_in_circle((0.0, 0.0), 9.0),
                start_alpha=255,
                duration1=random.uniform(0.6, 1.0),
                mid_alpha=0,
                duration2=random.uniform(0.1, 0.2),
                end_alpha=255,
                mutation_callback=firework_spark_mutator
            )
        )
        self.emitters.append(sparks)

def firework_spark_mutator(particle: arcade.FadeParticle):
    """mutation_callback shared by all fireworks sparks"""
    # gravity
    particle.change_y += -0.03
    # drag
    particle.change_x *= 0.92
    particle.change_y *= 0.92