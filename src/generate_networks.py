import networkx as nx


def create_er(n=1000, avg_degree=6):
    p = avg_degree / (n - 1)
    return nx.erdos_renyi_graph(n, p)


def create_ws(n=1000, k=6, rewiring=0.1):
    return nx.watts_strogatz_graph(n, k, rewiring)


def create_ba(n=1000, m=3):
    return nx.barabasi_albert_graph(n, m)