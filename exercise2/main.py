# remote module
import pandas
import random

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
random.seed(40)  # Testcase $4
# random.seed(52)  # Testcase $5
# random.seed(68)  # Testcase $6
# random.seed(73)  # Testcase $7
# random.seed(85)  # Testcase $8
# random.seed(91)  # Testcase $9
# random.seed(150) # Testcase $10

columns = ['nodes', 'penalty of flows', 'demand of nodes', ]
# function
'''
brief: initial all parameters in the objective function and constraints
para:   none
retval: none
'''


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


'''
brief: write the excel file
para:   path - the local path to the file
        sheet - the sheet need to be written
retval: none
'''


def write_file(path, sheet):
    df = pandas.DataFrame(list(zip(edge, p, d)), columns=columns)
    df.to_excel(path, sheet_name=sheet)

# main
initial()
write_file('data.xlsx', sheet='data')
print(edge)
# for i in range(12):
#     print(edge[i])

# local module
# import stage1
# import stage2