import math
import random
import arcade

import badwing.app
from badwing.brain import Brain

degRads = (math.pi*2)/360


def distance2d(start, end):
    diffX = start[0] - end[0]
    diffY = start[1] - end[1]
    return math.sqrt((diffX*diffX)+(diffY*diffY))    

class ButterflyBrain(Brain):
    def __init__(self, model):
        super().__init__(model)
        self.heading = 0
        self.wheel = 0
        self.begin_pos = (0,0)
        self.end_pos = (0,0)
        self.sensor_range = 512

    def update(self, delta_time):
        super().update(delta_time)
        if(self.at_goal()):
            pt = random.randint(0, 3)
            pd = random.randint(0, 45)
            if(pt == 0):
                self.left(pd)
            elif(pt == 2):
                self.right(pd)
            self.randforward()
        self.move()

    def at_goal(self):
        distance = distance2d(self.position, self.end_pos)
        return distance < 5

    def move_to(self, end_pos):
        self.begin_pos = self.position
        self.end_pos = end_pos

    def move(self):
        x, y = self.position
        to_x, to_y = self.end_pos

        pd = random.randint(0, 3)
        if(pd == 0):
            self.micro_left()
        elif(pd == 2):
            self.micro_right()

        steering_ndx = int(math.pi+(math.atan2(y - to_y, x - to_x)))
        delta = steering[steering_ndx][self.wheel]

        self.try_move(delta)

    def try_move(self, delta):
        delta_x, delta_y = delta
        next_x, next_y = 0, 0
        need_turn = False

        sprite = self.model.sprite
        min_x, max_x, min_y, max_y = sprite.left, sprite.right, sprite.top, sprite.bottom
        w_min_x, w_max_x, w_min_y, w_max_y = 0, 12800, 0, 600

        if(min_x < w_min_x):
            delta_x = -min_x
            need_turn = True
        elif(max_x > w_max_x):
            delta_x = w_max_x - max_x
            need_turn = True

        if(min_y < w_min_y):
            delta_y = w_min_y - min_y
            need_turn = True
        elif(max_y > w_max_y):
            delta_y = w_max_y - max_y
            need_turn = True

        #TODO:use pymunk
        if not need_turn:
            need_turn = collision_list = arcade.check_for_collision_with_list(self.sprite, badwing.app.level.ground_layer.sprites)

        if(need_turn):
            self.right(45)
            self.randforward()

        pos = self.position
        next_x = pos[0] + delta_x
        next_y = pos[1] + delta_y                    
        
        self.position = (next_x, next_y)
        sprite.change_x = pos[0] - next_x
        sprite.change_y = pos[1] - next_y

    def left(self, angle):
        heading = self.heading - angle
        self.heading = heading if heading > 0 else 360 + heading

    def right(self, angle):
        heading = self.heading + angle
        self.heading = heading if heading < 359 else heading - 360

    def micro_left(self):
        ph = self.wheel - 1
        if(ph < 0 ):
            ph = 0
        self.wheel = ph

    def micro_right(self):
        ph = self.wheel + 1
        if(ph > 2):
            ph = 2
        self.wheel = ph

    def forward(self, distance):
        x, y = self.position
        px = x+(distance*(math.cos(self.heading*degRads)))
        py = y+(distance*(math.sin(self.heading*degRads)))
        self.move_to((px, py))

    def randforward(self):
        self.forward(random.randint(0, self.sensor_range))

steering = [
    [(1, -1), (1, 0), (1, 1)],
    [(1, 0), (1, 1), (0, 1)],
    [(1, 1), (0, 1), (-1, 1)],
    [(0, 1), (-1, 1), (-1, 0)],
    [(-1, 1), (-1, 0), (-1, -1)],
    [(-1, 0), (-1, -1), (0, -1)],
    [(-1, -1), (0, -1), (1, -1)],
    [(0, -1), (1, -1), (1, 0)]
]
