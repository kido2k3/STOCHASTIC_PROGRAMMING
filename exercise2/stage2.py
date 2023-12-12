#%%
import stage1 as st1 

egde_of_G = [st1.G.edges[1, 2], st1.G.edges[1, 4], st1.G.edges[2, 3], st1.G.edges[2, 5], st1.G.edges[3, 6], st1.G.edges[4, 5],
             st1.G.edges[4, 7], st1.G.edges[5, 6], st1.G.edges[5, 8], st1.G.edges[6, 9], st1.G.edges[7, 8], st1.G.edges[8, 9]]
# min_scenario_cost = []

# for i in range(3):
#     for j in range(st1.G.number_of_edges()):
#         #Change attribute for edge after threshold for each scenario
#         egde_of_G[j]["weight"] = st1.MAIN.edge[0].cal_new_travel_time(st1.MAIN.TIME_THRESHOLD, st1.MAIN.scenario[i])
#         egde_of_G[j]["capacity"] = st1.MAIN.edge[0].cal_new_capacity(st1.MAIN.TIME_THRESHOLD, st1.MAIN.scenario[i])
#     #Calculate the min_cost for each scenario
#     minCostFlow = st1.nx.max_flow_min_cost(st1.G, 1, 9)
#     minCost = st1.nx.cost_of_flow(st1.G, minCostFlow)
#     min_scenario_cost.append(minCost)

# scenario_rate = [0.3, 0.4, 0.3]
# total_min_cost_2 = 0
# for i in range(3):
#     total_min_cost_2 = total_min_cost_2 + scenario_rate[i]*min_scenario_cost[i] 
# print("Min cost value after time threshold = " + str(total_min_cost_2))
# # %%
# print("Total min cost of two stage: " + str(total_min_cost_2 + st1.minCost))
# %%
# import main as MAIN

'''
Sample graph: 
1--->2--->3
|    |    |
4--->5--->6
|    |    |
7--->8--->9
'''

#Set data for nodes
node_data = []
for i in range(st1.MAIN.NUMBER_OF_VARIABLES):
    data = {
        "Code" : i + 1,
        "Time" : 0,
        "Car_amount" : 0
    }
    if i == 0:
        data["Car_amount"] = st1.MAIN.NUMBER_OF_CARS
    node_data.append(data)
def node_index(code):
    index = 0
    for i in range(st1.MAIN.NUMBER_OF_VARIABLES):
        if node_data[i]["Code"] == code:
            index = i
    return index

# The time before threshold
node_after_safe = []   #List of node use for temp source
safe_time = st1.MAIN.TIME_THRESHOLD
total_safe_flow = 0    #Go for plan stage 1 before time threshold

#Setting dfs algorithm with completing some tasks
def dfs_safe_path(node, time):
    for i in range(st1.MAIN.NUMBER_OF_EDGES):
        global total_safe_flow, node_data
        if st1.MAIN.edge[i].vertex_from == node:
            # Amount of cars expected to move in edge according to stage 1
            plan_flow = (st1.flowDict.get(st1.MAIN.edge[i].vertex_from)).get(st1.MAIN.edge[i].vertex_to)
            if(plan_flow) != 0:
                # Amount of cars in start node
                current_flow = node_data[node_index(st1.MAIN.edge[i].vertex_from)]["Car_amount"]
                # Calculate the current amount of cars moving
                if(current_flow < plan_flow):
                    plan_flow = current_flow
                    node_data[node_index(st1.MAIN.edge[i].vertex_from)]["Car_amount"] = 0
                else: 
                    node_data[node_index(st1.MAIN.edge[i].vertex_from)]["Car_amount"] = current_flow - plan_flow
                # Total cost and time after moving
                total_safe_flow = total_safe_flow + plan_flow * st1.MAIN.edge[i].penalty
                time = time + st1.MAIN.edge[i].penalty
                # Set data to arrived node
                node_data[node_index(st1.MAIN.edge[i].vertex_to)]["Car_amount"] = node_data[node_index(st1.MAIN.edge[i].vertex_to)]["Car_amount"] + plan_flow
                node_data[node_index(st1.MAIN.edge[i].vertex_to)]["Time"] = time
                print("Node to: " + str(st1.MAIN.edge[i].vertex_to))
                print(time)
                # Calculate the situation which cars arrived to sink
                if(st1.MAIN.edge[i].vertex_to != 9):
                    if time >= safe_time: 
                        print("Threshold reach! Return to Node: " + str(st1.MAIN.edge[i].vertex_from))
                        node_after_safe.append(node_data[node_index(st1.MAIN.edge[i].vertex_to)])
                    else: 
                        dfs_safe_path(st1.MAIN.edge[i].vertex_to, time)
                        print("Node current: " + str(st1.MAIN.edge[i].vertex_from))
                else: 
                    print("Flow reach sink!")
                    print("Amount of flow reached sink: " + str(node_data[node_index(st1.MAIN.edge[i].vertex_to)]["Car_amount"]))
                time = time - st1.MAIN.edge[i].penalty     
        else: 
            continue
    return

#Finding nodes after reached threshold
dfs_safe_path(1, 0)
print(node_data)
print("Total flow before reach threshold: " + str(total_safe_flow))

#Variation time to change data of edge
variation_time = 0
for i in range(len(node_after_safe)):
    if(node_after_safe[i]["Time"] > variation_time):
        variation_time = node_after_safe[i]["Time"]
print("Time when data change happened: " + str(variation_time))

#Remove duplicate arrived node after reached time threshold
del node_after_safe
node_after_safe = []
for i in range(st1.MAIN.NUMBER_OF_VARIABLES - 1):
    if node_data[i]["Car_amount"] > 0:
        node_after_safe.append(node_data[i])
print(node_after_safe)
