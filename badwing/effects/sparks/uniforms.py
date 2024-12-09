from ctypes import (
    Structure,
    c_float,
    sizeof,
)

from crunge.engine.uniforms import Vec2, Vec4

class Particle(Structure):
    _fields_ = [
        ("position", Vec2),
        ("velocity", Vec2),
        ("color", Vec4),
        ("age", c_float),
        ("lifespan", c_float),
        ("_pad1", c_float * 2),
    ]

assert sizeof(Particle) % 16 == 0
