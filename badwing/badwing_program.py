from loguru import logger
from jinja2 import PackageLoader

from crunge.engine.d2.program_2d import Program2D


class BadwingProgram(Program2D):
    def __init__(self) -> None:
        super().__init__([PackageLoader("badwing.resources", "shaders")])
