import random
import numpy as np

"""
n = number of agents
m = number of items
Runs picking sequence with f(t) = t + y
"""

def test(n, m, y):
    # randomize valuations
    vals = [[0]*m for i in range(n)]
    for i in range(n):
        for j in range(m):
            vals[i][j] = random.random() # uniform [0,1]
            #vals[i][j] = random.expovariate(1.0) # exponential with mean 1
            #vals[i][j] = random.lognormvariate(0.0, 1.0) # log normal with mu = 0, sigma = 1

    # define weights
    weights = [0]*n
    for i in range(n):
        #weights[i] = float(i+1)
        weights[i] = random.random()

    # compute each agent's normalized valuation of the complete set -- MC
    norm_tot_vals = np.divide(np.sum(vals, axis = 1), np.sum(weights))
    

    alloc = [-1]*m # indicates which item goes to which agent
    numpicks = [0]*n # number of times each agent has picked
    for i in range(m):
        # determine which agent should pick next
        nextagent = n-1 
        for j in range(n-2, -1, -1):
            ratio_j = (numpicks[j] + y) / weights[j]
            ratio_next = (numpicks[nextagent] + y) / weights[nextagent]
            if ratio_j < ratio_next - 1e-8:
                nextagent = j
        # determine which item this agent should pick
        nextitem = -1
        nextvalue = -1
        for j in range(m): 
            if alloc[j] == -1 and vals[nextagent][j] > nextvalue:
                nextitem = j
                nextvalue = vals[nextagent][j]
        alloc[nextitem] = nextagent
        numpicks[nextagent] += 1

    # check if the allocation is WPROP -- MC
    for i in range(n):
        vals_i = [0]*n # i's value for different bundles
        for j in range(m):
            vals_i[alloc[j]] += vals[i][j]
        weighted_val_i = vals_i[i]/weights[i]
        
        if weighted_val_i < norm_tot_vals[i] - 1e-8:
                return False
    return True

#############################

for i in range(4, 7): # number of agents
    for j in range(10, 35, 5): # number of items
        runs = 1000 # number of tries
        print(str(i) + " agents, " + str(j) + " items, " + str(runs) + " tries")
        for z in range(0, 105, 5): # y times 100
            y = z / 100.0
            count = 0
            for x in range(runs):
                if test(i, j, y):
                    count += 1
            print("y = " + str(y) + ": #WPROP = " + str(count))
