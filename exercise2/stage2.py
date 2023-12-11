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
node_after_safe = []   #List of node use for temp source
safe_time = st1.MAIN.TIME_THRESHOLD
total_safe_flow = 0    #Go for plan stage 1 before time threshold
print(st1.flowDict)

def dfs_safe_path(node, time):
    for i in range(st1.MAIN.NUMBER_OF_EDGES):
        global total_safe_flow
        if st1.MAIN.edge[i].vertex_from == node:
            plan_flow = (st1.flowDict.get(st1.MAIN.edge[i].vertex_from)).get(st1.MAIN.edge[i].vertex_to)
            if(plan_flow) != 0:
                total_safe_flow = total_safe_flow + plan_flow * st1.MAIN.edge[i].penalty
                time = time + st1.MAIN.edge[i].penalty
                print("Node to: " + str(st1.MAIN.edge[i].vertex_to))
                print(time)
                if(st1.MAIN.edge[i].vertex_to != 9):
                    if time >= safe_time: 
                        print("Threshold reach! Return to Node: " + str(st1.MAIN.edge[i].vertex_from))
                        node_data = {
                            "Code" : st1.MAIN.edge[i].vertex_to,
                            "Time" : time,
                            "Demand" : plan_flow
                        }
                        node_after_safe.append(node_data)
                    else: 
                        dfs_safe_path(st1.MAIN.edge[i].vertex_to, time)
                else: 
                    print("Flow reach sink!")
                    print("Amount of flow reached sink: " + str(plan_flow))
                time = time - st1.MAIN.edge[i].penalty
                    
        else: 
            continue
    return

dfs_safe_path(1, 0)
print("Total flow before reach threshold: " + str(total_safe_flow))
print(node_after_safe)
    

#Fold - Fulkerson algorithm in making residual network
# node = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# edge = MAIN.edge
# time = st1.MAIN.p
# demand = MAIN.d

# def Fold_Fulkerson(node, edge, time, demand):
# %%
