from crunge.engine.d2.physics import PhysicsMaterial

PLAYER = PhysicsMaterial("player", friction=0.3, restitution=0.0)

FEET = PhysicsMaterial("feet", friction=0.8, restitution=0.0)
FLOOR = PhysicsMaterial("floor", friction=0.8, restitution=0.0)

SHIP = PhysicsMaterial("ship", friction=0.3, restitution=0.2)
LASER = PhysicsMaterial("laser", friction=0.0, restitution=0.0)
METEOR = PhysicsMaterial("meteor", friction=0.5, restitution=0.4)
