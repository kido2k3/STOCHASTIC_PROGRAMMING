#%%
import pandas
import random
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from networkx.algorithms.flow import edmonds_karp
#Extensions used: Juypter (search in VsCode)
## Type "#%%" on top of the piece of code you want to run
#############################

# Global variables
ARRAY_TO_RANDOM = [1/2, 1/3, 1/4, 1, 1.25, 1.5, 1.75]
NUMBER_OF_CARS = 400


class Edge:
    # def __init__(self, vertex_from, vertex_to, time, capacity):
    #     self.vertex_from = vertex_from
    #     self.vertex_to = vertex_to
    #     self.penalty = time
    #     self.capacity = capacity

    def __init__(self, vertex_from, vertex_to):
        self.vertex_from = vertex_from
        self.vertex_to = vertex_to
        self.penalty = random.randint(1, 20)
        self.capacity = int(NUMBER_OF_CARS*random.choice(ARRAY_TO_RANDOM))
        # objective variables
        self.x = 0
        self.y = 0

    def cal_new_capacity(self, time, scenario, demand):
        if scenario == 'scenario1':
            seed = 34
        else: 
            seed = 22
        var = (self.capacity + time)*seed % 400
        while(var < demand): 
            var = var * 2 + demand
        return var

    def cal_new_travel_time(self, time, scenario):
        if scenario == 'scenario1':
            seed = 34
        else: 
            seed = 22
        return (self.penalty + time)*seed % 30

    def __repr__(self):
        return f'({self.vertex_from},{self.vertex_to}, p = {self.penalty}, c = {self.capacity})'


NUMBER_OF_VARIABLES = 9
NUMBER_OF_EDGES = 12
TIME_LENGTH = 150
TIME_THRESHOLD = 10
d = [0]*NUMBER_OF_VARIABLES
p = [0]*NUMBER_OF_EDGES
edge = []
scenario = ['scenario1', 'scenario2']

# random.seed(10)  # Testcase $1
# random.seed(25)  # Testcase $2
# random.seed(30)  # Testcase $3
# random.seed(40)  # Testcase $4
# random.seed(52)  # Testcase $5
# random.seed(68)  # Testcase $6
# random.seed(73)  # Testcase $7
# random.seed(85)  # Testcase $8
# random.seed(91)  # Testcase $9
random.seed(150) # Testcase $10

def initial():
    global d, edge, p

    d[0] = NUMBER_OF_CARS
    for i in range(NUMBER_OF_VARIABLES-2):
        d[i] = 0
    d[NUMBER_OF_VARIABLES - 1] = -NUMBER_OF_CARS

    # edge.append(Edge(1, 2, 7, 50))
    # edge.append(Edge(1, 4, 1, 100))

    # edge.append(Edge(2, 3, 4, 20))
    # edge.append(Edge(2, 5, 6, 30))

    # edge.append(Edge(3, 6, 1, 50))

    # edge.append(Edge(4, 5, 3, 30))
    # edge.append(Edge(4, 7, 2, 50))

    # edge.append(Edge(5, 6, 7, 30))
    # edge.append(Edge(5, 8, 3, 120))

    # edge.append(Edge(6, 9, 5, 100))
    # edge.append(Edge(7, 8, 5, 70))
    # edge.append(Edge(8, 9, 4, 120))

    edge.append(Edge(1, 2))
    edge.append(Edge(1, 4))

    edge.append(Edge(2, 3))
    edge.append(Edge(2, 5))

    edge.append(Edge(3, 6))

    edge.append(Edge(4, 5))
    edge.append(Edge(4, 7))

    edge.append(Edge(5, 6))
    edge.append(Edge(5, 8))

    edge.append(Edge(6, 9))
    edge.append(Edge(7, 8))
    edge.append(Edge(8, 9))

    for i in range(len(edge)):
        p[i] = edge[i].penalty

    edge = sorted(edge, key=lambda x: x.vertex_from)

initial()

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
def init():
    G = nx.DiGraph() # Create a graph with 0 node
    #Create node
    G.add_node(1, demand=-NUMBER_OF_CARS, color="#c53d46")
    # G.add_node(1, demand=-100, color="#c53d46")
    G.add_node(2, demand=0, color="#fff8b6")
    G.add_node(3, demand=0, color="#fff8b6")
    G.add_node(4, demand=0, color="#fff8b6")
    G.add_node(5, demand=0, color="#fff8b6")
    G.add_node(6, demand=0, color="#fff8b6")
    G.add_node(7, demand=0, color="#fff8b6")
    G.add_node(8, demand=0, color="#fff8b6")
    # G.add_node(9, demand=100, color="#b0e0e6")
    G.add_node(9, demand=NUMBER_OF_CARS, color="#b0e0e6")

    #Create link between each node according to sample graph
    for i in range(NUMBER_OF_EDGES):
        G.add_edge(edge[i].vertex_from, edge[i].vertex_to, weight=edge[i].penalty, capacity=edge[i].capacity, flow = 0)

    # G.add_edge(1, 2, weight=7, capacity=50, flow=0)
    # G.add_edge(1, 4, weight=1, capacity=100, flow=0)

    # G.add_edge(2, 3, weight=4, capacity=20, flow=0)
    # G.add_edge(2, 5, weight=6, capacity=30, flow=0)

    # G.add_edge(3, 6, weight=1, capacity=50, flow=0)

    # G.add_edge(4, 5, weight=3, capacity=30, flow=0)
    # G.add_edge(4, 7, weight=2, capacity=50, flow=0)

    # G.add_edge(5, 6, weight=7, capacity=30, flow=0)
    # G.add_edge(5, 8, weight=3, capacity=120, flow=0)

    # G.add_edge(6, 9, weight=5, capacity=100, flow=0)
    # G.add_edge(7, 8, weight=3, capacity=70, flow=0)
    # G.add_edge(8, 9, weight=4, capacity=120, flow=0)

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
    return (G, node_post)
def drawGraph(G, node_postition):
    edge_capacity = nx.get_edge_attributes(G, "capacity")
    edge_weight = nx.get_edge_attributes(G, "weight")
    node_colors = list(nx.get_node_attributes(G, "color").values())
    nx.draw(G, pos=node_post, with_labels=True, font_color='red', node_size=800, node_color=node_colors)
    # nx.draw_networkx_edge_labels(G, pos=node_post, edge_labels=edge_capacity)
    nx.draw_networkx_edge_labels(G, pos=node_postition, edge_labels=edge_capacity)
    return True
def calculate(G):
    flowCost, flowDict = nx.capacity_scaling(G)
    return flowCost, flowDict
def updateGraph(G, edge, attribute, value):
    nx.set_edge_attributes(G, {edge: {attribute: value}})
#Initialize and draw a graph
G, node_post = init()
drawGraph(G, node_post)
#%%
#Find optimal solution for max flow
flowCost, flowDict = calculate(G)
for node in flowDict:
    print(str(node) + "->" + str(flowDict[node]))
print("Cost of flow: " + str(flowCost))
