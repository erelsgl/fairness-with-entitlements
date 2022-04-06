import random
import prtpy

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

    sumweights = sum(weights)

    for i in range(n):
        # Compute i's MMS:
        MMS = prtpy.partition(
            algorithm=prtpy.partitioning.integer_programming,
            numbins=n,
            items=vals[i],
            objective=prtpy.obj.MinimizeLargestSum,
            outputtype=prtpy.out.LargestSum
        )
        NMMS = MMS * (n * weights[i] / sumweights)


        # try all partitions to compute i's NMMS
        part = [0]*m
        NMMS = 0.0
        while True: # compute i's NMMS
            worst_bundle_val = 1e10
            vals_i = [0]*n # i's value for different bundles
            for j in range(m):
                vals_i[part[j]] += vals[i][j]
            NMMS_candidate = min(vals_i)
            # normalize NMMS
            NMMS_candidate *= (n * weights[i] / sumweights)
            if NMMS < NMMS_candidate - 1e-8:
                NMMS = NMMS_candidate
            # go to next partition
            j = m-1
            while True:
                if part[j] != n-1:
                    part[j] += 1
                    break
                part[j] = 0
                j -= 1
                if j == -1: # we have tried all partitions
                    break
            if j == -1:
                break
        # compute i's value from actual allocation
        real_vals_i = 0
        for j in range(m):
            if alloc[j] == i:
                real_vals_i += vals[i][j]
        # check if i gets at least i's WMMS
        if real_vals_i < NMMS - 1e-8:
            return False
    return True
                

#############################

for i in range(3, 4): # number of agents
    for j in range(4, 12, 2): # number of items
        runs = 10000 # number of tries
        print(str(i) + " agents, " + str(j) + " items, " + str(runs) + " tries")
        for z in range(0, 105, 5): # y times 100
            y = z / 100.0
            count = 0
            for x in range(runs):
                if test(i, j, y):
                    count += 1
            #print("y = " + str(y) + ": " + str(count))
            print("(" + str(y) + "," + str(count/100.0) + ")", sep='', end='')
        print("")
