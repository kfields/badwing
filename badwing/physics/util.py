import pymunk

def check_grounding(player):
    """ See if the player is on the ground. Used to see if we can jump. """
    grounding = {
        'normal': pymunk.Vec2d.zero(),
        'penetration': pymunk.Vec2d.zero(),
        'impulse': pymunk.Vec2d.zero(),
        'position': pymunk.Vec2d.zero(),
        'body': None
    }

    def f(arbiter):
        n = -arbiter.contact_point_set.normal
        if n.y > grounding['normal'].y:
            grounding['normal'] = n
            grounding['penetration'] = -arbiter.contact_point_set.points[0].distance
            grounding['body'] = arbiter.shapes[1].body
            grounding['impulse'] = arbiter.total_impulse
            grounding['position'] = arbiter.contact_point_set.points[0].point_b

    player.body.each_arbiter(f)

    return grounding

from arcade import check_for_collision_with_list
from arcade import check_for_collision
from arcade import Sprite
from arcade import SpriteList


def _circular_check(player, walls):
    """
    This is a horrible kludge to 'guess' our way out of a collision
    Returns:

    """
    original_x = player.center_x
    original_y = player.center_y

    vary = 1
    while True:
        try_list = [[original_x, original_y + vary],
                    [original_x, original_y - vary],
                    [original_x + vary, original_y],
                    [original_x - vary, original_y],
                    [original_x + vary, original_y + vary],
                    [original_x + vary, original_y - vary],
                    [original_x - vary, original_y + vary],
                    [original_x - vary, original_y - vary]
                    ]

        for my_item in try_list:
            x, y = my_item
            player.center_x = x
            player.center_y = y
            check_hit_list = check_for_collision_with_list(player, walls)
            # print(f"Vary {vary} ({self.player_sprite.center_x} {self.player_sprite.center_y}) "
            #       f"= {len(check_hit_list)}")
            if len(check_hit_list) == 0:
                return
        vary *= 2
