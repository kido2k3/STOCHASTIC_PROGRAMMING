#%%
import stage1 as st1 

'''
Sample graph: 
1--->2--->3
|    |    |
4--->5--->6
|    |    |
7--->8--->9
'''

#Handle cost before time threshold
#Set data for nodes
node_data = []
for i in range(st1.NUMBER_OF_VARIABLES):
    data = {
        "Code" : i + 1,
        "Time" : 0,
        "Car_amount" : 0
    }
    if i == 0:
        data["Car_amount"] = st1.NUMBER_OF_CARS
    node_data.append(data)
def node_index(code):
    index = 0
    for i in range(st1.NUMBER_OF_VARIABLES):
        if node_data[i]["Code"] == code:
            index = i
    return index

# The time before threshold
node_after_safe = []   #List of node use for temp source
safe_time = st1.TIME_THRESHOLD
total_safe_flow = 0    #Go for plan stage 1 before time threshold

#Setting dfs algorithm with completing some tasks
def dfs_safe_path(node, time):
    for i in range(st1.NUMBER_OF_EDGES):
        global total_safe_flow, node_data
        if st1.edge[i].vertex_from == node:
            # Amount of cars expected to move in edge according to stage 1
            plan_flow = (st1.flowDict.get(st1.edge[i].vertex_from)).get(st1.edge[i].vertex_to)
            if(plan_flow) != 0:
                # Amount of cars in start node
                current_flow = node_data[node_index(st1.edge[i].vertex_from)]["Car_amount"]
                # Calculate the current amount of cars moving
                if(current_flow < plan_flow):
                    plan_flow = current_flow
                    node_data[node_index(st1.edge[i].vertex_from)]["Car_amount"] = 0
                else: 
                    node_data[node_index(st1.edge[i].vertex_from)]["Car_amount"] = current_flow - plan_flow
                # Total cost and time after moving
                total_safe_flow = total_safe_flow + plan_flow * st1.edge[i].penalty
                time = time + st1.edge[i].penalty
                # Set data to arrived node
                node_data[node_index(st1.edge[i].vertex_to)]["Car_amount"] = node_data[node_index(st1.edge[i].vertex_to)]["Car_amount"] + plan_flow
                node_data[node_index(st1.edge[i].vertex_to)]["Time"] = time
                    # print("Node to: " + str(st1.edge[i].vertex_to))
                    # print(time)
                # Calculate the situation which cars arrived to sink
                if(st1.edge[i].vertex_to != 9):
                    if time >= safe_time: 
                        # print("Threshold reach! Return to Node: " + str(st1.edge[i].vertex_from))
                        node_after_safe.append(node_data[node_index(st1.edge[i].vertex_to)])
                    else: 
                        dfs_safe_path(st1.edge[i].vertex_to, time)
                        # print("Node current: " + str(st1.edge[i].vertex_from))
                else: 
                    # print("Flow reach sink!")
                    # print("Amount of flow reached sink: " + str(node_data[node_index(st1.edge[i].vertex_to)]["Car_amount"]))
                    node_after_safe.append(node_data[node_index(st1.edge[i].vertex_to)])
                time = time - st1.edge[i].penalty     
        else: 
            continue
    return

#Finding nodes after reached threshold
dfs_safe_path(1, 0)
# print(node_data)
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
for i in range(st1.NUMBER_OF_VARIABLES - 1):
    if node_data[i]["Car_amount"] > 0:
        node_after_safe.append(node_data[i])
print("Source nodes after reached time threshold: ")
print(node_after_safe)

#%%
#Handle cost after time threshold
#Create a temp super source to include all nodes which have cars
cars_remain = 0
for i in range(st1.NUMBER_OF_VARIABLES - 1):
    if node_data[i]["Car_amount"] > 0:
        cars_remain = cars_remain + node_data[i]["Car_amount"]

st1.G.add_node(0, demand=-cars_remain, color="#ffff00") #Node temp(Code: 0)
st1.node_post[0] = (1/2, 1/2) #Node position
for i in range(st1.NUMBER_OF_VARIABLES - 1):
    if node_data[i]["Car_amount"] > 0:
        st1.G.add_edge(0, node_data[i]["Code"], weight = 0, capacity = node_data[i]["Car_amount"], flow = 0)

#Change data after time threshold through scenario
#Change node data
st1.G.nodes[1]["demand"] = 0
st1.G.nodes[9]["demand"] = st1.G.nodes[9]["demand"] - node_data[8]["Car_amount"]

# print(st1.G.nodes[0]["demand"])
# print(st1.G.nodes[1]["demand"])
# print(st1.G.nodes[9]["demand"])

#Change edge data
egde_of_G = [st1.G.edges[1, 2], st1.G.edges[1, 4], st1.G.edges[2, 3], st1.G.edges[2, 5], st1.G.edges[3, 6], st1.G.edges[4, 5],
             st1.G.edges[4, 7], st1.G.edges[5, 6], st1.G.edges[5, 8], st1.G.edges[6, 9], st1.G.edges[7, 8], st1.G.edges[8, 9]]
min_scenario_cost = []

#Calculate the min cost when cars move after threshold in each scenario
for i in range(len(st1.scenario)):
    for j in range(st1.NUMBER_OF_EDGES):
        #Change attribute for edge after threshold for each scenario
        egde_of_G[j]["weight"] = st1.edge[j].cal_new_travel_time(variation_time, st1.scenario[i])
        egde_of_G[j]["capacity"] = st1.edge[j].cal_new_capacity(variation_time, st1.scenario[i], cars_remain / 2)
        # print("Capacity of " + str(st1.edge[j].vertex_from) + " -> " + str(st1.edge[j].vertex_to) + ": " + str(egde_of_G[j]["capacity"]))
    #Calculate the min_cost for each scenario
    cost, dict = st1.calculate(st1.G)
    st1.drawGraph(st1.G, st1.node_post)
    print("Possible min cost path in scenario " + str(i + 1))
    for node in dict:
        print(str(node) + "->" + str(dict[node]))
    # print(dict)
    print("Cost of part after time threshold in scenario " + str(i + 1) + ": " + str(cost))
    min_scenario_cost.append(cost)

#Calculate the average min cost when cars move after threshold
scenario_rate = [0.5, 0.5]
total_after_flow = 0
for i in range(len(st1.scenario)):
    total_after_flow = total_after_flow + scenario_rate[i]*min_scenario_cost[i] 
print("Min cost value after time threshold through several scenarios: " + str(total_after_flow))

#%%
#Total min cost in subploblem 2 and draw graph
print("Total min cost of two stage: " + str(total_safe_flow + total_after_flow))
st1.drawGraph(st1.G, st1.node_post)

# %%
