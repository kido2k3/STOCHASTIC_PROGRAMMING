# remote module
import pandas
import random

# local module
import stage1
import stage2
# Global variables
NUMBER_OF_VARIABLES = 85
NUMBER_OF_CARS = 400
x = []
y = []
c = []
p = []
u = []
d = []
scenes = []
random.seed(40)
columns = ['penalty of flows','demand of nodes']
# function
'''
brief: initial all parameters in the objective function and constraints
para:   none
retval: none
'''
def initial():
    global p, d
    for i in range(NUMBER_OF_VARIABLES):
        p.append(2)
    d.append(NUMBER_OF_CARS)
    for i in range(NUMBER_OF_VARIABLES-2):
        d.append(0)
    d.append(-NUMBER_OF_CARS)
'''
brief: write the excel file
para:   path - the local path to the file
        sheet - the sheet need to be written
retval: none
'''
def write_file(path, sheet):
    df = pandas.DataFrame(list(zip(p,d)), columns=columns)
    df.to_excel(path, sheet_name=sheet)


# main
initial()
write_file('data.xlsx', sheet='data')