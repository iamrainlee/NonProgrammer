import logging
import json
import copy

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/parasite', methods=['POST'])
def parasite():
    data = request.get_json()
    logging.info("Data: {}".format(data))
    result = []
    for i in data:
        result.append(calparasite(i))
    logging.info("My result :{}".format(result))
    return json.dumps(result)

def calparasite(data):
    r = {}
    r["room"] = data["room"]
    r["p1"] = {}
    for i in data['interestedIndividuals']:
        r["p1"][i] = -1
    grid = []
    for i in data['grid']:
        grid.append(i.copy())
    grid2 = []
    for i in data['grid']:
        grid2.append(i.copy())
    changed = True
    tick = 0
    tick2 = 0
    while changed:
        changed1 = False
        changed2 = False
        oldgrid = copy.deepcopy(grid)
        # for i in grid:
        #     oldgrid.append(i.copy())
        oldgrid2 = copy.deepcopy(grid2)
        # for i in grid2:
        #     oldgrid2.append(i.copy())
        # oldgrid[0][0] = 4
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if(oldgrid[i][j] == 3):
                    try:
                        if(grid[i+1][j] == 1):
                            grid[i+1][j] = 3
                            changed1 = True
                    except:
                        a = 1
                    try:
                        if(grid[i][j+1] == 1):
                            grid[i][j+1] = 3
                            changed1 = True
                    except:
                        a = 1
                    try:
                        if(grid[i-1][j] == 1 and (i-1) >= 0):
                            grid[i-1][j] = 3
                            changed1 = True
                    except:
                        a = 1
                    try:
                        if(grid[i][j-1] == 1 and (j-1) >= 0):
                            grid[i][j-1] = 3
                            changed1 = True
                    except:
                        a = 1
                if(oldgrid2[i][j] == 3):
                    try:
                        if(grid2[i+1][j] == 1):
                            grid2[i+1][j] = 3
                            changed2 = True
                    except:
                        a = 1
                    try:
                        if(grid2[i][j+1] == 1):
                            grid2[i][j+1] = 3
                            changed2 = True
                    except:
                        a = 1
                    if((i-1) >= 0):
                        if(grid2[i-1][j] == 1):
                            grid2[i-1][j] = 3
                            changed2 = True
                        try:
                            if(grid2[i-1][j+1] == 1):
                                grid2[i-1][j+1] = 3
                                changed2 = True
                        except:
                            a = 1
                    if((j-1) >= 0):
                        if(grid2[i][j-1] == 1):
                            grid2[i][j-1] = 3
                            changed2 = True
                        try:
                            if(grid2[i+1][j-1] == 1):
                                grid2[i+1][j-1] = 3
                                changed2 = True
                        except:
                            a = 1
                        if((i-1) >= 0):
                            if(grid2[i-1][j-1] == 1):
                                grid2[i-1][j-1] = 3
                                changed2 = True
                    try:
                        if(grid2[i+1][j+1] == 1):
                            grid2[i+1][j+1] = 3
                            changed2 = True
                    except:
                        a = 1
        if(changed1):
            tick += 1
            for p1 in r["p1"]:
                ind = [int(i) for i in p1.split(',')]
                if(data['grid'][ind[0]][ind[1]] != 1):
                    continue
                elif(r["p1"][p1] == -1):
                    if(grid[ind[0]][ind[1]] == 3):
                        r["p1"][p1] = tick
        if(changed2):
            tick2 += 1
        # logging.info("grid2: {}".format(grid2))
        changed = changed1 or changed2
    uninfected1 = False
    uninfected2 = False
    energy = 1000000
    uninfecteds = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if(grid[i][j] == 1):
                uninfected1 = True
                uninfecteds.append((i,j))
            if(grid2[i][j] == 1):
                uninfected2 = True
    if(uninfected1):
        for k in uninfecteds:
            grid3 = copy.deepcopy(grid)
            e = getenergy(grid3,k[0],k[1])
            energy = min(calenergy(grid3,k[0],k[1],e),energy)
    else:
        energy = 0
    if(uninfected1):
        r["p2"] = -1
    else:
        r["p2"] = tick
    if(uninfected2):
        r["p3"] = -1
    else:
        r["p3"] = tick2
    r["p4"] = energy
    return r

def changedGraph(grid,i,j):
    try:
        if(grid[i+1][j] == 1):
            grid[i+1][j] = 3
            changedGraph(grid,i+1,j)
    except:
        a = 1
    try:
        if(grid[i-1][j] == 1 and (i-1) >= 0):
            grid[i-1][j] = 3
            changedGraph(grid,i-1,j)
    except:
        a = 1
    try:
        if(grid[i][j+1] == 1):
            grid[i][j+1] = 3
            changedGraph(grid,i,j+1)
    except:
        a = 1
    try:
        if(grid[i][j-1] == 1 and (j-1)>=0):
            grid[i][j-1] = 3
            changedGraph(grid,i,j-1)
    except:
        a = 1

def getenergy(grid3,i,j):
    if(grid3[i][j]!=1):
        return 0
    tenergy = 100
    success = False
    for k in range(1,len(grid3)):
        if(tenergy<=k):
            break
        try:
            if(grid3[i+k+1][j] == 3):
                tenergy = min(k,tenergy)
                success = True
        except:
            a = 1
        try:
            if((i-k-1) >= 0 and grid3[i-k-1][j] == 3):
                tenergy = min(k,tenergy)
                success = True
        except:
            a = 1
        try:
            if(grid3[i][j+k+1] == 3):
                tenergy = min(k,tenergy)
                success = True
        except:
            a = 1
        try:
            if((j-k-1) >= 0 and grid3[i][j-k-1] == 3):
                tenergy = min(k,tenergy)
                success = True
        except:
            a = 1

        try:
            if(grid3[i+k][j+k] == 3):
                tenergy = min(k+k-1,tenergy)
                success = True
        except:
            a = 1
        try:
            if((j-k) >= 0 and grid3[i+k][j-k] == 3):
                tenergy = min(k+k-1,tenergy)
                success = True
        except:
            a = 1
        if((i-k)>=0):
            try:
                if(j-k) >= 0 and grid3[i-k][j-k] == 3:
                    tenergy = min(k+k-1,tenergy)
                    success = True
            except:
                a = 1
            try:
                if((i-k) >= 0 and grid3[i-k][j+k] == 3 ):
                    tenergy = min(k+k-1,tenergy)
                    success = True
            except:
                a = 1
        for l in range(1,k):
            try:
                if(grid3[i+k][j+l] == 3):
                    tenergy = min(k+l-1,tenergy)
                    success = True
            except:
                a = 1
            if(j-l)>=0:
                try:
                    if(grid3[i+k][j-l] == 3):
                        tenergy = min(k+l-1,tenergy)
                        success = True
                except:
                    a = 1
                if((i-k) >= 0 and grid3[i-k][j-l] == 3):
                    tenergy = min(k+l-1,tenergy)
                    success = True
            try:
                if((i-k) >= 0 and grid3[i-k][j+l] == 3):
                    tenergy = min(k+l-1,tenergy)
                    success = True
            except:
                a = 1
            if(i-l) >= 0:
                if((j-k) >= 0 and grid3[i-l][j-k] == 3):
                    tenergy = min(k+l-1,tenergy)
                    success = True
                try:
                    if(grid3[i-l][j+k] == 3):
                        tenergy = min(k+l-1,tenergy)
                        success = True
                except:
                    a = 1
            try:
                if((j-k) >= 0 and grid3[i+l][j-k] == 3):
                    tenergy = min(k+l-1,tenergy)
                    success = True
            except:
                a = 1
            try:
                if(grid3[i+l][j+k] == 3):
                    tenergy = min(k+l-1,tenergy)
                    success = True
            except:
                a = 1
    if(success):
        grid3[i][j] = 3
        changedGraph(grid3,i,j)
        return tenergy
    else:
        return -1
def calenergy(grid,i,j,score):
    # score = getenergy(grid,i,j)
    uninfecteds = []
    uninfected = False
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if(grid[i][j] == 1):
                uninfected = True
                uninfecteds.append((i,j))
    if(not uninfected):
        return score
    energys = []
    ind = []

    for k in uninfecteds:
        grid4 = copy.deepcopy(grid)
        energys.append(getenergy(grid4,k[0],k[1]))
        ind.append((k[0],k[1]))
    x = energys.index(min(energys))
    y = getenergy(grid,ind[x][0],ind[x][1])
    if(len(energys)==0):
        return score
    return calenergy(grid,ind[x][0],ind[x][1],y) + score
