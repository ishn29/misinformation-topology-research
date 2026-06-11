import json
import random
from pathlib import Path

import pandas as pd

from src.generate_networks import create_er, create_ws, create_ba
from src.simulation import run_simulation
from src.metrics import calculate_metrics


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)


def run_baseline_experiments(trials=100, n=1000, beta=0.15, gamma=0.05):
    results = []
    all_curves = []

    network_builders = {
        "ER": lambda: create_er(n=n, avg_degree=6),
        "WS": lambda: create_ws(n=n, k=6, rewiring=0.1),
        "BA": lambda: create_ba(n=n, m=3),
    }

    for topology, builder in network_builders.items():
        print(f"Running {topology}...")

        for trial in range(trials):
            random.seed(trial)

            G = builder()

            sim_result = run_simulation(
                G,
                beta=beta,
                gamma=gamma,
                initial_infected_count=5
            )

            metrics = calculate_metrics(sim_result, n=n)

            results.append({
                "topology": topology,
                "trial": trial,
                "n": n,
                "beta": beta,
                "gamma": gamma,
                **metrics
            })

            all_curves.append({
                "topology": topology,
                "trial": trial,
                "infected_counts": sim_result["infected_counts"]
            })

    return pd.DataFrame(results), all_curves


def main():
    results_df, all_curves = run_baseline_experiments()

    results_path = DATA_DIR / "baseline_results.csv"
    curves_path = DATA_DIR / "baseline_curves.json"

    results_df.to_csv(results_path, index=False)

    with open(curves_path, "w") as f:
        json.dump(all_curves, f)

    print(f"Saved results to {results_path}")
    print(f"Saved curves to {curves_path}")

    print(results_df.groupby("topology")[["t10", "t50", "peak_infected", "final_size", "auc"]].mean())


if __name__ == "__main__":
    main()