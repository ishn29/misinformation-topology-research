import pandas as pd
import random

from src.generate_networks import create_er, create_ws, create_ba
from src.simulation import run_simulation
from src.metrics import calculate_metrics


def run_baseline_experiments(trials=100, n=1000, beta=0.15, gamma=0.05):
    results = []

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

            row = {
                "topology": topology,
                "trial": trial,
                "n": n,
                "beta": beta,
                "gamma": gamma,
                **metrics
            }

            results.append(row)

    return pd.DataFrame(results)


def main():
    df = run_baseline_experiments()

    df.to_csv("data/baseline_results.csv", index=False)

    print("Saved results to data/baseline_results.csv")
    print(df.groupby("topology")[["t10", "t50", "peak_infected", "final_size", "auc"]].mean())


if __name__ == "__main__":
    main()