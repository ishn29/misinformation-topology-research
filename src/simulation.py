import random


SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2


def run_simulation(G, beta=0.15, gamma=0.05, initial_infected_count=5, immune_nodes=None, max_steps=500):
    """
    Runs an SIR-style misinformation spread simulation.

    S = has not seen misinformation
    I = actively spreading misinformation
    R = stopped spreading / corrected
    """

    if immune_nodes is None:
        immune_nodes = set()
    else:
        immune_nodes = set(immune_nodes)

    nodes = list(G.nodes())

    possible_initial = [node for node in nodes if node not in immune_nodes]

    if len(possible_initial) < initial_infected_count:
        raise ValueError("Not enough non-immune nodes to infect initially.")

    states = {node: SUSCEPTIBLE for node in nodes}

    for node in immune_nodes:
        states[node] = RECOVERED

    initial_infected = random.sample(possible_initial, initial_infected_count)

    for node in initial_infected:
        states[node] = INFECTED

    infected_counts = []
    recovered_counts = []
    total_ever_infected = set(initial_infected)

    for step in range(max_steps):
        infected_nodes = [node for node in nodes if states[node] == INFECTED]

        infected_counts.append(len(infected_nodes))
        recovered_counts.append(sum(1 for node in nodes if states[node] == RECOVERED))

        if len(infected_nodes) == 0:
            break

        new_infections = []
        new_recoveries = []

        for node in infected_nodes:
            for neighbor in G.neighbors(node):
                if states[neighbor] == SUSCEPTIBLE:
                    if random.random() < beta:
                        new_infections.append(neighbor)

            if random.random() < gamma:
                new_recoveries.append(node)

        for node in new_infections:
            states[node] = INFECTED
            total_ever_infected.add(node)

        for node in new_recoveries:
            states[node] = RECOVERED

    return {
        "infected_counts": infected_counts,
        "recovered_counts": recovered_counts,
        "total_ever_infected": len(total_ever_infected),
        "steps": len(infected_counts)
    }