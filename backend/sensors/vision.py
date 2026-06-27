from backend.sensors.raycast import cast_ray
import math

class Vision:
    def __init__(self, ray_count=8, max_range=200.0):
        self.ray_count = ray_count
        self.max_range = max_range
    
    def sense(self, animal, world):
        observations = []
        angle_step = 2 * math.pi / self.ray_count

        for i in range(self.ray_count):
            angle = animal.direction + i * angle_step
            entity, distance = cast_ray(
                origin = animal.position,
                direction = angle,
                world = world,
                source = animal,
                max_range = self.max_range
            )

            ray = {
                "distance": self.max_range,
                "plant": False,
                "herbivore": False,
                "carnivore": False
            }

            if entity is not None:
                ray["distance"] = distance

                if entity.species == "plant":
                    ray["plant"] = True
                elif entity.species == "herbivore":
                    ray["herbivore"] = True
                elif entity.species == "carnivore":
                    ray["carnivore"] = True
                
            observations.append(ray)
            
        return observations