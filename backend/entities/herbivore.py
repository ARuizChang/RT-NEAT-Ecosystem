from .animal import Animal

class Herbivore(Animal):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.species = "herbivore"
        self.radius = 3.0 