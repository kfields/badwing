from loguru import logger

from crunge.engine.d2.particle.system import ParticleSystem2D
from crunge.engine.d2.particle.spawner import RadialBurstSpawner

from .sparks_program import SparksProgram


class SparksVu(ParticleSystem2D):
    def __init__(self, color=(0.0, 0.0, 1.0, 1.0)):
        super().__init__(program=SparksProgram(), color=color)

    def create_spawner(self):
        self.spawner = RadialBurstSpawner(self.color, lifespan=50.0)
