import random
import networkx as nx


def select_random_nodes(G, fraction):
    k = int(G.number_of_nodes() * fraction)
    return set(random.sample(list(G.nodes()), k))


def select_high_degree_nodes(G, fraction):
    k = int(G.number_of_nodes() * fraction)
    degrees = sorted(G.degree(), key=lambda x: x[1], reverse=True)
    return set(node for node, degree in degrees[:k])


def select_high_betweenness_nodes(G, fraction):
    k = int(G.number_of_nodes() * fraction)
    betweenness = nx.betweenness_centrality(G)
    ranked = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
    return set(node for node, score in ranked[:k])


def get_fact_checking_nodes(G, strategy, fraction):
    if strategy == "none":
        return set()
    elif strategy == "random":
        return select_random_nodes(G, fraction)
    elif strategy == "degree":
        return select_high_degree_nodes(G, fraction)
    elif strategy == "betweenness":
        return select_high_betweenness_nodes(G, fraction)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")