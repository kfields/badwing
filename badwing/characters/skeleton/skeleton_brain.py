import math
import random
import arcade

from botsley.run.task import *

import badwing.app
from badwing.brain import Brain

class SkeletonBrain(Brain):
    def __init__(self, model):
        super().__init__(model)

        with selector() as top:
            with condition(SeesPlayer) as sees:
                with action() as a:
                    async def fn(task, msg):
                        while True:
                            self.move_to(sees.position)
                    a.use(fn)
            with action() as a:
                async def fn(task, msg):
                    print('b count: ', q.count)
                a.use(fn)

        self.tree = top

class SkeletonBrain(Brain):
    def __init__(self, model):
        super().__init__(model)
        with root() as root:
            with sensor(See):
                pass
            with selector():
                with condition(_I, _see_enemy) as sees:                
                    with action() as a:
                        async def fn(task, msg):
                            while True:
                                self.move_to(sees.position)
                        a.use(fn)
                with action() as a:
                    async def fn(task, msg):
                        print('b count: ', q.count)
                    a.use(fn)

        self.schedule(root)
