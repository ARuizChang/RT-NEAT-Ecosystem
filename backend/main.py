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


def main():
    world = World(size=(2000, 2000))
    observation_builder = ObservationBuilder(ray_count=8, max_range=200.0)
    rtneat = RTNEAT(population_size=50, num_inputs=28, num_outputs=5)
    rtneat.initialize()

    dt = 0.05
    for tick in range(100000):
        simulate_step(world, dt, observation_builder, rtneat)


if __name__ == "__main__":
    main()