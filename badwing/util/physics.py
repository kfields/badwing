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
