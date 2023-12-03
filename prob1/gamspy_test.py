import numpy as np
import gamspy as gms
import scipy.stats as stats
import sys


# Set the seed for reproducibility
np.random.seed(0)

# Parameters
n = 8  # Number of products
m = 5  # Number of parts to be ordered before production

# b_min, b_max = 100, 200
# l_min, l_max = 50, 100
# q_min, q_max = 0, 50 
# s_min, s_max = 0, 50 
# A_min, A_max = 0, 10 

# Simulate data for matrix A and vectors b, l, q, s
A = np.random.randint(0, 10**7, size=(n, m))  # Randomly simulated matrix A of size n x m
b = np.random.randint(10, 10**9, m)  # Vector b
l = np.random.randint(5, 10**9, n)  # Vector l
q = np.random.randint(10, 10**8, n)  # Vector q
s = np.random.randint(1, 10**9, m)  # Vector s
# stats.binom.rvs()

# A = np.random.randint(A_min, A_max, size=(n, m))  # Randomly simulated matrix A of size n x m
# b = np.random.randint(b_min, b_max, m)  # Vector b
# l = np.random.randint(l_min, l_max, n)  # Vector l
# q = np.random.randint(q_min, q_max, n)  # Vector q
# s = np.random.randint(s_min, s_max, m)  # Vector s

# Assumed bounds for decision variables z, you need to provide this based on your scenario
d1 = stats.binom.rvs(10, 0.5, size=n)
d2 = stats.binom.rvs(10, 0.5, size=n, random_state = 1)

print(d1)
print(d2)

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

A_param = ct.addParameter('A', [i, j], A)
d1_param = ct.addParameter('d1', i, d1)
d2_param = ct.addParameter('d2', i, d2)

# print(A_param.records)
# print(d1_param.records)
# print(d2_param.records)
# print(b_param.records)
# print(l_param.records)
# print(q_param.records)
# print(s_param.records)

# Create variable
x = gms.Variable(container=ct, name="x", domain=j, type="Positive", description="the numbers of parts to be ordered before production")
y1 = gms.Variable(container=ct, name="y1", domain=j, type="Positive", description="the number of parts left in inventory for s1")
z1 = gms.Variable(container=ct, name="z1", domain=i, type="Positive", description="the number of units produced for s1")
y2 = gms.Variable(container=ct, name="y2", domain=j, type="Positive", description="the number of parts left in inventory for s2")
z2 = gms.Variable(container=ct, name="z2", domain=i, type="Positive", description="the number of units produced for s2")

# x = gms.Variable(container=ct, name="x", domain=j, type="Integer", description="the numbers of parts to be ordered before production")
# y1 = gms.Variable(container=ct, name="y1", domain=j, type="Integer", description="the number of parts left in inventory for s1")
# z1 = gms.Variable(container=ct, name="z1", domain=i, type="Integer", description="the number of units produced for s1")
# y2 = gms.Variable(container=ct, name="y2", domain=j, type="Integer", description="the number of parts left in inventory for s2")
# z2 = gms.Variable(container=ct, name="z2", domain=i, type="Integer", description="the number of units produced for s2")

# Define equation 
e1 = gms.Equation(container=ct, name="first_stage", domain=j)
e2 = gms.Equation(container=ct, name="units_produced_s1", domain=i, description="range of units produced of product i for s1")
e3 = gms.Equation(container=ct, name="parts_left_s1", domain=j, description="number of parts left for s1")
e4 = gms.Equation(container=ct, name="units_produced_s2", domain=i, description="range of units produced of product i for s2")
e5 = gms.Equation(container=ct, name="parts_left_s2", domain=j, description="number of parts left for s2")

e1[j] = gms.Sum(i, A_param[i, j] * x[j]) == b_param[j]
e2[i] = z1[i] <= d1_param[i] 
e3[j] = y1[j] == x[j] - gms.Sum(i, A_param[i, j] * z1[i])
e4[i] = z2[i] <= d2_param[i]
e5[j] = y2[j] == x[j] - gms.Sum(i, A_param[i, j] * z2[i])

#Define objective
obj = gms.Sum(j, b_param[j] * x[j]) + 1/2 * gms.Sum(i, (l_param[i] - q_param[i]) * z1[i]) - gms.Sum(j, s_param[j] * y1[j]) + 1/2 * gms.Sum(i, (l_param[i] - q_param[i]) * z2[i]) - gms.Sum(j, s_param[j] * y2[j])
# #Define model
transport = gms.Model(container=ct, name="transport", equations=ct.getEquations(), problem="LP", sense=gms.Sense.MIN, objective=obj)
# transport = gms.Model(container=ct, name="transport", equations=ct.getEquations(), problem="MIP", sense=gms.Sense.MIN, objective=obj)

transport.solve()

print(ct.describeVariables())
# print(x.records)
# print(z1.records)
# print(d1)
# print(d2)