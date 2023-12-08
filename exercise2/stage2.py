#%%
import stage1 as st1 

egde_of_G = [st1.G.edges[1, 2], st1.G.edges[1, 4], st1.G.edges[2, 3], st1.G.edges[2, 5], st1.G.edges[3, 6], st1.G.edges[4, 5],
             st1.G.edges[4, 7], st1.G.edges[5, 6], st1.G.edges[5, 8], st1.G.edges[6, 9], st1.G.edges[7, 8], st1.G.edges[8, 9]]
min_scenario_cost = []

for i in range(3):
    for j in range(st1.G.number_of_edges()):
        #Change attribute for edge after threshold for each scenario
        egde_of_G[j]["weight"] = st1.MAIN.edge[0].cal_new_travel_time(st1.MAIN.TIME_THRESHOLD, st1.MAIN.scenario[i])
        egde_of_G[j]["capacity"] = st1.MAIN.edge[0].cal_new_capacity(st1.MAIN.TIME_THRESHOLD, st1.MAIN.scenario[i])
    #Calculate the min_cost for each scenario
    minCostFlow = st1.nx.max_flow_min_cost(st1.G, 1, 9)
    minCost = st1.nx.cost_of_flow(st1.G, minCostFlow)
    min_scenario_cost.append(minCost)

scenario_rate = [0.3, 0.4, 0.3]
total_min_cost_2 = 0
for i in range(3):
    total_min_cost_2 = total_min_cost_2 + scenario_rate[i]*min_scenario_cost[i] 
print("Min cost value after time threshold = " + str(total_min_cost_2))
# %%
print("Total min cost of two stage: " + str(total_min_cost_2 + st1.minCost))

# %%
