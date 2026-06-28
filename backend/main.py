from pathlib import Path
import sys

# Make the repository root importable when this file is run directly
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.simulation.world import World
from backend.sensors.observation_builder import ObservationBuilder
from backend.neural.rtneat import RTNEAT
from backend.simulation.update_loop import simulate_step

from backend.persistence.checkpoints import save_checkpoint, load_checkpoint
from backend.persistence.save_population import save_population
from backend.persistence.load_population import load_population


def main():
    world = World(size=(2000, 2000))
    observation_builder = ObservationBuilder(ray_count=8, max_range=200.0)
    rtneat = RTNEAT(population_size=50, num_inputs=28, num_outputs=5)
    rtneat.initialize()

    dt = 0.05
    for tick in range(10000000):
        simulate_step(world, dt, observation_builder, rtneat)
        if tick % 1000000:
            save_checkpoint(world, rtneat, "data/checkpoints/latest.json")
    save_population(rtneat, "data/saves/population.json")

if __name__ == "__main__":
    main()