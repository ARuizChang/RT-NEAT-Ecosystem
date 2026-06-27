import math
from typing import Optional, Tuple

def cast_ray(origin, direction, world, source=None, max_range=200.0):
    x, y = origin
    angle = direction

    dx = math.cos(angle)
    dy = math.sin(angle)

    for step in range(int(max_range)):
        tx = x + dx * step
        ty = y + dy * step

        for entity in world.entities.values():
            if entity is source:
                continue
            dist = math.hypot(tx - entity.pos[0], ty - entity.pos[1])
            if dist <= entity.radius:
                return entity, step / max_range
    
    return None, 1.0