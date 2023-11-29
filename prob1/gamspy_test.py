import numpy as np
import gamspy as gms
import scipy.stats as stats
import sys


# Set the seed for reproducibility
np.random.seed(0)

# Parameters
n = 8  # Number of products
m = 5  # Number of parts to be ordered before production
num_scenarios = 2  # Number of scenarios

# Simulate data for matrix A and vectors b, l, q, s
A = np.random.randint(0, 10**9, size=(n, m))  # Randomly simulated matrix A of size n x m
b = np.random.randint(10, 10**9, m)  # Vector b
l = np.random.randint(5, 10**9, n)  # Vector l
q = np.random.randint(10, 10**9, n)  # Vector q
s = np.random.randint(1, 10**9, m)  # Vector s
# c = l - q  # Cost coefficients

# small_value = 1e-10
# A_modified = np.where(A == 0, small_value, A)

# Assumed bounds for decision variables z, you need to provide this based on your scenario
d = stats.binom.rvs(10, 0.5, size=n)

# Create contain
ct = gms.Container()

# Create set
i = gms.Set(container=ct, name="i", records=["Pr" + str(p) for p in range(1, n+1)], description="products") 
j = gms.Set(container=ct, name="j", records=["Pa" + str(p) for p in range(1, m+1)], description="parts")

# Create parameter
b_param = ct.addParameter('b', j, b)
l_param = ct.addParameter('l', i, l)
q_param = ct.addParameter('q', i, q)
s_param = ct.addParameter('s', j, s)
# A_param = ct.addParameter('A', [i, j], A_modified)
A_param = ct.addParameter('A', [i, j], A)
d_param = ct.addParameter('d', i, d)

# print(A_param.records)
print(d_param.records)
# print(b_param.records)
# print(l_param.records)
# print(q_param.records)
# print(s_param.records)

# Create variable
x = gms.Variable(container=ct, name="x", domain=j, type="Positive", description="the numbers of parts to be ordered before production")
y1 = gms.Variable(container=ct, name="y", domain=j, type="Positive", description="the number of parts left in inventory")
z1 = gms.Variable(container=ct, name="z", domain=i, type="Positive", description="the number of units produced")
y2 = gms.Variable(container=ct, name="y", domain=j, type="Positive", description="the number of parts left in inventory")
z2 = gms.Variable(container=ct, name="z", domain=i, type="Positive", description="the number of units produced")

# Define equation 
e1 = gms.Equation(container=ct, name="first_stage", domain=j)
# e2 = gms.Equation(container=ct, name="units_produced_s1", domain=i, description="range of units produced of product i for s1")
# e3 = gms.Equation(container=ct, name="parts_left_s1", domain=j, description="number of parts left for s1")
# e4 = gms.Equation(container=ct, name="units_produced_s2", domain=i, description="range of units produced of product i for s2")
# e5 = gms.Equation(container=ct, name="parts_left_s2", domain=j, description="number of parts left for s2")

e1[j] = gms.Sum(i, A_param[i, j] * x[j]) == b_param[j]
# e2[i] = z1[i] <= d_param[i]
# e3[j] = y1[j] == x[j] - gms.Sum(i, A_param[i, j] * z1[i])
# e4[i] = z2[i] <= d_param[i]
# e5[j] = y2[j] == x[j] - gms.Sum(i, A_param[i, j] * z2[i])


#Define objective
obj = gms.Sum(j, b_param[j] * x[j]) #+ 1/2 * gms.Sum(i, (l_param[i] - q_param[i]) * z1[i]) - gms.Sum(j, s_param[j] * y1[j]) + 1/2 * gms.Sum(i, (l_param[i] - q_param[i]) * z2[i]) - gms.Sum(j, s_param[j] * y2[j])

# #Define model
transport = gms.Model(container=ct, name="transport", equations=ct.getEquations(), problem="LP", sense=gms.Sense.MIN, objective=obj)

# transport.solve(output=sys.stdout)
transport.solve()

print(x.records)

# Define variables
# z = [model.add_variable(f"z{i}", lb=0, ub=d[i], vartype=gms.VarType.CONTINUOUS) for i in range(n)]
# y = [model.add_variable(f"y{j}", lb=0, vartype=gms.VarType.CONTINUOUS) for j in range(m)]

# Define the objective function
# objective = sum(c[i] * z[i] for i in range(n)) + sum(s[j] * y[j] for j in range(m))
# model.set_objective(objective, sense=gms.Sense.MINIMIZE)

# # Define constraints for y = x - sum(A^T * z)
# for j in range(m):
#     model.add_constraint(y[j] == b[j] - sum(A[i][j] * z[i] for i in range(n)))

# # Solve the model
# model.solve()

# # Retrieve results
# print("Optimal solution:")
# for i in range(n):
#     print(f"z[{i}] = {z[i].level}")
# for j in range(m):
#     print(f"y[{j}] = {y[j].level}")
# print(f"Objective value: {model.get_objective().value}")


# import gamspy as gp
# import numpy as np
# import pandas as pd
# import scipy.stats as stats

# #---------- 1. Tạo dữ liệu mô phỏng ----------#

# # Số lượng sản phẩm và bộ phận
# n = 8
# m = 5

# # Tạo ma trận A (kích thước 8x5) - Số lượng bộ phận cần thiết cho mỗi sản phẩm
# a = np.random.randint(0, 10, size=(n, m))

# # Tạo vector b, l, q, s
# b = np.random.randint(10, 50, size=m)     # Giới hạn số lượng bộ phận có sẵn
# l = np.random.uniform(5, 20, size=n)   # Chi phí thêm để sản xuất mỗi sản phẩm
# q = np.random.uniform(10, 30, size=n)  # Giá bán cho mỗi sản phẩm
# s = np.random.uniform(1, 5, size=m)       # Giá trị phế liệu cho mỗi bộ phận không sử dụng

# # Tạo nhu cầu D - Mỗi phần tử tuân theo phân phối nhị thức Bin(10, 1/2)
# D = stats.binom.rvs(10, 0.5, size=n)

# #---------- 2. Xây dựng mô hình số hóa ----------#

# # Tạo container
# ct = gp.Container()

# i = gp.Set(ct, "i", records=["P" + str(p) for p in range(1, n+1)], description="Products")
# j = gp.Set(ct, "j", records=["P" + str(p) for p in range(1, m+1)], description="Parts")

# b_param = ct.addParameter('b', j, b)
# l_param = ct.addParameter('l', i, l)
# q_param = ct.addParameter('q', i, q)
# s_param = ct.addParameter('s', j, s)
# A_param = ct.addParameter('A', [i, j], a)

# x = gp.Variable(ct, name="x", domain=[j])
# y = gp.Variable(ct, name="y", domain=[j])
# z = gp.Variable(ct, name="z", domain=[i])

# model = gp.Model(ct, name="slp", problem="LP")
# print(A_param.records)