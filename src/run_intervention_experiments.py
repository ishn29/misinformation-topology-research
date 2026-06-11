import json
import random
from pathlib import Path

import pandas as pd

from src.generate_networks import create_er, create_ws, create_ba
from src.simulation import run_simulation
from src.metrics import calculate_metrics
from src.interventions import get_fact_checking_nodes


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)


def run_intervention_experiments(
    trials=100,
    n=1000,
    beta=0.15,
    gamma=0.05
):
    results = []
    all_curves = []

    network_builders = {
        "ER": lambda: create_er(n=n, avg_degree=6),
        "WS": lambda: create_ws(n=n, k=6, rewiring=0.1),
        "BA": lambda: create_ba(n=n, m=3),
    }

    strategies = ["none", "random", "degree", "betweenness"]
    fractions = [0.00, 0.01, 0.05, 0.10]

    for topology, builder in network_builders.items():
        for strategy in strategies:
            for fraction in fractions:

                if strategy == "none" and fraction != 0.00:
                    continue

                if strategy != "none" and fraction == 0.00:
                    continue

                print(f"Running {topology}, {strategy}, fraction={fraction}")

                for trial in range(trials):
                    random.seed(trial)

                    G = builder()

                    immune_nodes = get_fact_checking_nodes(
                        G,
                        strategy=strategy,
                        fraction=fraction
                    )

                    sim_result = run_simulation(
                        G,
                        beta=beta,
                        gamma=gamma,
                        initial_infected_count=5,
                        immune_nodes=immune_nodes
                    )

                    metrics = calculate_metrics(sim_result, n=n)

                    results.append({
                        "topology": topology,
                        "strategy": strategy,
                        "fraction": fraction,
                        "trial": trial,
                        "n": n,
                        "beta": beta,
                        "gamma": gamma,
                        **metrics
                    })

                    all_curves.append({
                        "topology": topology,
                        "strategy": strategy,
                        "fraction": fraction,
                        "trial": trial,
                        "infected_counts": sim_result["infected_counts"]
                    })

    return pd.DataFrame(results), all_curves


def main():
    results_df, all_curves = run_intervention_experiments()

    results_path = DATA_DIR / "intervention_results.csv"
    curves_path = DATA_DIR / "intervention_curves.json"

    results_df.to_csv(results_path, index=False)

    with open(curves_path, "w") as f:
        json.dump(all_curves, f)

    print(f"Saved results to {results_path}")
    print(f"Saved curves to {curves_path}")

    print(
        results_df.groupby(["topology", "strategy", "fraction"])[
            ["t50", "peak_infected", "final_size", "auc"]
        ].mean()
    )


if __name__ == "__main__":
    main()