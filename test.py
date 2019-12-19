import networkx as nx
from rank_swirl import *
G = nx.gnp_random_graph(n=50, p=5/50, directed=True)
nx2rankfigure(G)