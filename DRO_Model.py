from gurobipy import *
import numpy as np
import random
import math

model=Model('humanitarian')

x = {}
v = {}
y = {}
q = {}
w = {}
u = {}


for k in K:
    name = 'x_' + str(k)
    x[k] = model.addVar(vtype=GRB.BINARY, name=name)

for k in K:
    name = 'v_' + str(k)
    v[k] = model.addVar(vtype=GRB.CONTINUOUS,lb = 0, ub = GRB.INFINITY, name=name)


for n in N:
    name = 'y_' + str(n)
    y[n] = model.addVar(vtype=GRB.BINARY, name=name)


for s in S:
    for k in K:
        for i in I:
            name = 'q_' + str(k) + '_' + str(i) + '_' + str(s)
            q[k,i,s] = model.addVar(vtype=GRB.CONTINUOUS,lb = 0, ub = GRB.INFINITY, name=name)


for s in S:
    for n in N:
        for i in I:
            name = 'w_' + str(n) + '_' + str(i)+ '_' + str(s)
            w[n,i,s] = model.addVar(vtype=GRB.CONTINUOUS,lb = 0, ub = GRB.INFINITY, name=name)


for s in S:
    for i in I:
        name = 'u_' + str(i)+ '_' + str(s)
        u[i,s] = model.addVar(vtype=GRB.CONTINUOUS, name=name)



Delta = {}
Gamma = {}
Theta = {}
Lambda = {}
alpha = {}
beta = {}
for s in S:
    for n in N:
        name = 'Delta_' + str(n)+ '_' + str(s)
        Delta[n,s] = model.addVar(vtype=GRB.CONTINUOUS, lb = 0, ub = GRB.INFINITY, name=name)

for s in S:
    for n in N:
        name = 'Gamma_' + str(n) + '_' + str(s)
        Gamma[n, s] = model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name=name)

for s in S:
    for n in N:
        name = 'Theta_' + str(n) + '_' + str(s)
        Theta[n, s] = model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name=name)

for s in S:
    for n in N:
        name = 'Lambda_' + str(n) + '_' + str(s)
        Lambda[n, s] = model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name=name)

for s in S:
    for n in N:
        name = 'beta_' + str(n) + '_' + str(s)
        beta[n, s] = model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name=name)

for s in S:
    for n in N:
        name = 'alpha_' + str(n) + '_' + str(s)
        alpha[n, s] = model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY, name=name)


Xi = {}
Pi = {}
Phi = {}
Psi = {}
delta = {}
gamma = {}
for s in S:
    for i in I:
        name = 'Xi_' + str(i)+ '_' + str(s)
        Xi[i,s] =  model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name=name)

for s in S:
    for i in I:
        name = 'Pi_' + str(i)+ '_' + str(s)
        Pi[i,s] =  model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name=name)

for s in S:
    for i in I:
        name = 'Phi_' + str(i)+ '_' + str(s)
        Phi[i,s] =  model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name=name)

for s in S:
    for i in I:
        name = 'Psi_' + str(i)+ '_' + str(s)
        Psi[i,s] =  model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name=name)

for s in S:
    for i in I:
        name = 'delta_' + str(i)+ '_' + str(s)
        delta[i,s] =  model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name=name)

for s in S:
    for i in I:
        name = 'gamma_' + str(i)+ '_' + str(s)
        gamma[i,s] =  model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY, name=name)

model.update()

obj_open = LinExpr(0)
for k in K:
    obj_open.addTerms(c_open,x[k])


obj_inventory = LinExpr(0)
for k in K:
    obj_inventory.addTerms(c_inventory, v[k])


obj_contract= LinExpr(0)
for n in N:
    obj_contract.addTerms(c_contract,y[n])


obj_tran_1 = LinExpr(0)
for k in K:
    for i in I:
        for s in S:
            obj_tran_1.addTerms(c_tra_1 * distance[i-1][k-1],q[k,i,s])


obj_tran_2 = LinExpr(0)
for n in N:
    for i in I:
        for s in S:
            obj_tran_2.addTerms(c_tra_2  * distance[i-1][n-1],w[n,i,s])


obj_penalty = LinExpr(0)
for i in I:
    for s in S:
        obj_penalty.addTerms(c_penalty,u[i,s])



obj_additional = LinExpr(0)
for n in N:
    for s in S:
        obj_additional.addTerms(max_supply_set[s-1][n-1],Delta[n,s])
        obj_additional.addTerms(-min_supply_set[s-1][n-1],Gamma[n,s])
        obj_additional.addTerms(mean_supply_set[s-1][n-1],Theta[n,s])
        obj_additional.addTerms(-mean_supply_set[s-1][n-1],Lambda[n,s])
        obj_additional.addTerms(mean_supply_set[s-1][n-1],alpha[n,s])
        obj_additional.addTerms(mad_supply_set[s-1][n-1],beta[n,s])

for i in I:
    for s in S:
        obj_additional.addTerms(max_demand_set[s-1][i-1],Xi[i,s])
        obj_additional.addTerms(-min_demand_set[s-1][i-1],Pi[i,s])
        obj_additional.addTerms(mean_demand_set[s-1][i-1],Phi[i,s])
        obj_additional.addTerms(-mean_demand_set[s-1][i-1],Psi[i,s])
        obj_additional.addTerms(mean_demand_set[s-1][i-1],gamma[i,s])
        obj_additional.addTerms(mad_demand_set[s-1][i-1],delta[i,s])
model.setObjective(obj_open + obj_contract + obj_inventory + (obj_tran_1 + obj_tran_2 + obj_penalty + obj_additional)/len(S),GRB.MINIMIZE)




for k in K:
    model.addConstr(v[k] <= Q_warehouse * x[k])

model.addConstr(quicksum(v[k] for k in K) <= Total)

for s in S:
    for k in K:
        model.addConstr(quicksum(q[k,i,s] for i in I) <=v[k])

for n in N:
    for s in S:
        model.addConstr(quicksum(w[n,i,s] for i in I) <= min_supply_set[s-1][n-1] * y[n])

for s in S:
    for i in I:
        model.addConstr(quicksum(q[k,i,s] for k in K) + u[i,s] + quicksum(w[n,i,s] for n in N) >= max_demand_set[s-1][i-1])


for n in N:
    for s in S:
        model.addConstr(Delta[n,s] - Gamma[n,s] + Theta[n,s] - Lambda[n,s] == -alpha[n,s])

for n in N:
    for s in S:
        model.addConstr(Theta[n, s] + Lambda[n, s] == beta[n, s])

for i in I:
    for s in S:
        model.addConstr(Xi[i,s] - Pi[i,s] + Phi[i,s] - Psi[i,s] == -gamma[i,s])

for i in I:
    for s in S:
        model.addConstr(Phi[i,s] + Psi[i,s] == delta[i,s])


model.optimize()


