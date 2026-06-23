from .entity import Entity

class Plant(Entity):
    def __init__(self, position=(0.0, 0.0), energy=20.0, regeneration_rate=0.1, max_energy=100.0):
        super().__init__(position=position, energy=energy)
        self.species = "plant"
        self.regeneration_rate = regeneration_rate
        self.max_energy = max_energy
        self.radius = 2.0
    
    def update(self, delta_time: float):
        self.energy = min(self.energy + self.regeneration_rate * delta_time, self.max_energy)
        self.age += delta_time

    def harvest(self, amount: float):
        taken = min(amount, self.energy)
        self.energy -= taken
        return taken