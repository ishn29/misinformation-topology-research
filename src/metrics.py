import numpy as np


def time_to_fraction_infected(infected_counts, n, fraction):
    threshold = n * fraction

    for t, count in enumerate(infected_counts):
        if count >= threshold:
            return t

    return None


def calculate_metrics(simulation_result, n):
    infected_counts = simulation_result["infected_counts"]

    peak_infected = max(infected_counts)
    t10 = time_to_fraction_infected(infected_counts, n, 0.10)
    t50 = time_to_fraction_infected(infected_counts, n, 0.50)
    auc = np.trapezoid(infected_counts)
    final_size = simulation_result["total_ever_infected"] / n

    return {
        "t10": t10,
        "t50": t50,
        "peak_infected": peak_infected,
        "auc": auc,
        "final_size": final_size,
        "duration": simulation_result["steps"]
    }