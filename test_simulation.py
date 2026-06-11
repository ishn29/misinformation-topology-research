from src.generate_networks import create_ba
from src.simulation import run_simulation
from src.metrics import calculate_metrics
import random

random.seed(42)

G = create_ba(n=1000, m=3)

result = run_simulation(
    G,
    beta=0.15,
    gamma=0.05,
    initial_infected_count=5
)

metrics = calculate_metrics(result, n=1000)

print(metrics)
print(result["infected_counts"][:20])