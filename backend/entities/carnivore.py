from .animal import Animal

class Carnivore(Animal):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.species = "carnivore"
        self.radius = 5.0
        self.attack_power = 20.0