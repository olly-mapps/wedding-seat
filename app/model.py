'''
Gurobi Model
'''


import numpy as np
import pandas as pd
import gurobipy as gp
from gurobipy import GRB
import json 

def run_model(param, relationships_matrix_raw):

    '''
    Parameters
    '''

    guest_count = param["guest_count"]
    child_count = param["child_count"]
    table_size = param["table_size"]
    child_table_size = param["child_table_size"]

    table_count = int(guest_count/table_size)

    if child_table_size != 0:
        child_table_count = int(child_count/child_table_size)
    else:
        child_table_count = 0

    relationships_matrix = np.array(relationships_matrix_raw)
    '''
    Parameter Sets
    '''

    GUESTS = [guest for guest in range(guest_count)]
    CHILDREN = [child for child in range(guest_count, guest_count+child_count)]
    TABLES = [table for table in range(table_count)]
    CHILD_TABLES = [child_table for child_table in range(table_count, table_count+child_table_count)]

    '''
    Environment and Model
    '''
    
    with open("gurobi_lic.json") as f:
        lic = json.load(f)


    env = gp.Env(empty = True)
    env.setParam('WLSACCESSID', lic["WLSACCESSID"])
    env.setParam('WLSSECRET', lic["WLSSECRET"])
    env.setParam('LICENSEID', int(lic["LICENSEID"]))

    env.start()

    m = gp.Model("wedding-seat", env = env)

    #m = gp.Model("wedding-seat")

    '''
    Decision Variables
    '''

    table_plan = m.addMVar((table_count+child_table_count, guest_count+child_count), vtype = GRB.BINARY)

    same_table = m.addMVar((guest_count+child_count, guest_count+child_count, table_count+child_table_count), vtype = GRB.BINARY)

    table_unhappiness = gp.LinExpr();

    for t in TABLES:
        table_unhappiness += gp.quicksum([relationships_matrix[i,j] * same_table[i,j,t] for i in GUESTS for j in GUESTS]);

    m.setObjective(table_unhappiness, GRB.MINIMIZE);

    '''
    Constraints
    '''

    ##Each guest must be assigned to a table
    for guest in GUESTS + CHILDREN:
        m.addConstr(gp.quicksum([table_plan[table,guest] for table in TABLES+CHILD_TABLES]) == 1)

    ##Each table must be at most table_size big
    for table in TABLES:
        m.addConstr(gp.quicksum([table_plan[table,guest] for guest in GUESTS]) == table_size) 

    ##Each child table must be at most child_table_size big
    for child_table in CHILD_TABLES:
        m.addConstr(gp.quicksum([table_plan[child_table,child] for child in CHILDREN]) == child_table_size)

    ##Adults and children sat apart (aka children sit exclusively with children)
    for adult in GUESTS:
        for child in CHILDREN:
            for table in TABLES + CHILD_TABLES:
                m.addConstr(same_table[adult,child,table] == 0)
            
    m.addConstr(table_plan[0,0] * table_plan[0,1] == 1)

    ##Links the table plan with the indicator variable array
    for g1 in GUESTS:
        for g2 in GUESTS:
            for t in TABLES:
                m.addConstr(same_table[g1,g2,t] == table_plan[t, g1] * table_plan[t, g2])


    '''
    Run Model
    '''

    m.optimize()

    '''
    Return
    '''

    return {"Table Plan": table_plan.X.tolist(), "Plan Unhappiness": m.objVal}