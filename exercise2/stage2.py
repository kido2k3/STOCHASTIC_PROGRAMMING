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

# The time before threshold
node_after_safe = []
safe_time = st1.MAIN.TIME_THRESHOLD

def dfs_safe_path(node, time):
    for i in range(st1.MAIN.NUMBER_OF_EDGES):
        if st1.MAIN.edge[i].vertex_from == node: 
            if((st1.flowDict.get(st1.MAIN.edge[i].vertex_from)).get(st1.MAIN.edge[i].vertex_to)) != 0:
                time = time + st1.MAIN.edge[i].penalty
                if time >= safe_time: 
                    print(time)
                    node_after_safe.append(st1.MAIN.edge[i].vertex_to)
                    time = time - st1.MAIN.edge[i].penalty
                else: 
                    print(st1.MAIN.edge[i].vertex_to)
                    print(time)
                    dfs_safe_path(st1.MAIN.edge[i].vertex_to, time)
                    time = time - st1.MAIN.edge[i].penalty
        else: 
            continue
    return

dfs_safe_path(1, 0)
print(node_after_safe)
    

#Fold - Fulkerson algorithm in making residual network
# node = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# edge = MAIN.edge
# time = st1.MAIN.p
# demand = MAIN.d

# def Fold_Fulkerson(node, edge, time, demand):
    

# %%
