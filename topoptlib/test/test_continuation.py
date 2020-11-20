#!/usr/bin/python3

# Author: Thijs Smit, June 2020
# Copyright (C) 2020 ETH Zurich

# Disclaimer:
# The authors reserves all rights but does not guaranty that the code is
# free from errors. Furthermore, we shall not be liable in any event
# caused by the use of the program.

import topoptlib
import numpy as np

data = topoptlib.Data()
data.structuredGrid((0.0, 2.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0), (129, 65, 65))
Emin, Emax, nu, dens, penal = 1.0e-9, 1.0, 0.3, 1.0, 1.0
data.material(Emin, Emax, nu, dens, penal)
data.filter(1, 0.08)
# setup continuation of penalization: (Pinitial, Pfinal, stepsize) update of penal every 10 iterations
data.continuation(1.0, 3.0, 1.0)
data.mma(40)
data.loadcases(1)
data.bc(0, 1, [0, 0], [0, 1, 2], [0.0, 0.0, 0.0], 0)
data.bc(0, 2, [0, 1, 2, 4], [2], [-0.001], 0)
data.bc(0, 2, [0, 1, 1, 2, 2, 4], [2], [-0.0005], 0)
data.bc(0, 2, [0, 1, 1, 3, 2, 4], [2], [-0.0005], 0)

materialvolumefraction = 0.12
nEl = data.nElements

def objective(comp, sumXp):
    return comp

def sensitivity(xp, uKu):
    return -1.0 * penal * np.power(xp, (penal - 1)) * (Emax - Emin) * uKu

def constraint(comp, sumXp):
    return sumXp / nEl - materialvolumefraction

def constraintSensitivity(xp, uKu):
    return 1.0 / nEl

data.obj(objective)
data.objsens(sensitivity)
data.cons(constraint)
data.conssens(constraintSensitivity)
data.initialcondition(materialvolumefraction)

# get a function to run for testing
def Test(trueFX, runtime, memory):
    
    trueFX = int(trueFX*1000)/1000
    print('trueFX: ',trueFX)

    if trueFX == 13.278:
        open("test_beam_continuation SUCCESFULL","w+")
    else:
        open("test_beam_ccontinuation not succesfull!","w+")

data.check(Test)

complete = data.solve()