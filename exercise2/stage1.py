#%%
import main as MAIN
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

#Extensions used: Juypter (search in VsCode)
## Type "#%%" on top of the piece of code you want to run
#############################

#set plot attributes
plt_size = 20
plt_width = 8
plt_height = 5

params = {
    "legend.fontsize": "large", 
    "figure.figsize": (plt_width, plt_height),
    "axes.labelsize": plt_size, 
    "axes.titlesize": plt_size,
    "xtick.labelsize": plt_size * 0.75,
    "ytick.labelsize": plt_size * 0.75,
    "axes.titlepad": 25
}

plt.rcParams.update(params)

'''
Sample graph: 
1--->2--->3
|    |    |
4--->5--->6
|    |    |
7--->8--->9
'''

G = nx.DiGraph() # Create a graph with 0 node
#Create node
G.add_node(1, demand=-MAIN.NUMBER_OF_CARS, color="#c53d46")
G.add_node(2, demand=0, color="#fff8b6")
G.add_node(3, demand=0, color="#fff8b6")
G.add_node(4, demand=0, color="#fff8b6")
G.add_node(5, demand=0, color="#fff8b6")
G.add_node(6, demand=0, color="#fff8b6")
G.add_node(7, demand=0, color="#fff8b6")
G.add_node(8, demand=0, color="#fff8b6")
G.add_node(9, demand=MAIN.NUMBER_OF_CARS, color="#b0e0e6")

#Create link between each node according to sample graph
for i in range(12):
    G.add_edge(MAIN.edge[i].vertex_from, MAIN.edge[i].vertex_to, weight=MAIN.edge[i].penalty, capacity=MAIN.edge[i].capacity)

# G.add_edge(1, 2, weight=2, capacity=50)
# G.add_edge(1, 4, weight=2, capacity=100)

# G.add_edge(2, 3, weight=2, capacity=20)
# G.add_edge(2, 5, weight=2, capacity=30)

# G.add_edge(3, 6, weight=2, capacity=50)

# G.add_edge(4, 5, weight=2, capacity=30)
# G.add_edge(4, 7, weight=2, capacity=50)

# G.add_edge(5, 8, weight=2, capacity=120)
# G.add_edge(5, 6, weight=2, capacity=30)

# G.add_edge(6, 9, weight=2, capacity=100)
# G.add_edge(7, 8, weight=2, capacity=70)
# G.add_edge(8, 9, weight=2, capacity=120)


#Plot the graph
node_post = {
    1: (-1, 1),
    2: (0, 1), 
    3: (1, 1), 
    4: (-1, 0), 
    5: (0, 0), 
    6: (1, 0), 
    7: (-1, -1), 
    8: (0, -1), 
    9: (1, -1)
}

edge_capacity = nx.get_edge_attributes(G, "capacity")
edge_weight = nx.get_edge_attributes(G, "weight")
node_colors = list(nx.get_node_attributes(G, "color").values())
nx.draw(G, pos=node_post, with_labels=True, font_color='red', node_size=800, node_color=node_colors)
# nx.draw_networkx_edge_labels(G, pos=node_post, edge_labels=edge_capacity)
nx.draw_networkx_edge_labels(G, pos=node_post, edge_labels=edge_capacity)

#%%
#Find feasible solution for max flow
from networkx.algorithms.flow import edmonds_karp
flowCost, flowPath = nx.maximum_flow(G, 1, 9, flow_func = edmonds_karp)
print(flowCost)
for node in flowPath: 
    print(str(node) + "->" + str(flowPath[node]))


#nx.draw(G, pos=node_post, with_labels=True, font_color='red', node_size=800, node_color=node_colors)
#nx.draw_networkx_edge_labels(G, pos=node_post, edge_labels=)
minCostFlow = nx.max_flow_min_cost(G, 1, 9)
minCost = nx.cost_of_flow(G, minCostFlow)
print("Min cost value: "+str(minCost))

# %%
