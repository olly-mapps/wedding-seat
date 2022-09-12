'''
Scripts
'''



import csv 
import os
import pandas as pd
import numpy as np
from scipy.sparse import dok_matrix
import ast

'''
Function to process csv input upon upload
'''

def process_csv(csv_input):

    csv_list_and_names=[]

    with open(csv_input) as f:
        df = pd.read_csv(f, encoding = "utf-8")
    
    df.fillna(0, inplace = True)
    names = df['Guest']
    df.drop(['Guest'], axis = 1, inplace = True)
    csv_list = df.values.tolist()

    csv_list_and_names.append(csv_list)
    csv_list_and_names.append(names.tolist())
    return csv_list_and_names

'''
Function to transfer string input to suitable numbers
'''

def rel_name_to_number(name_dict):

    name_dict.popitem()
    name_dict = {eval(k):v for k,v in name_dict.items()}

    rel_name_to_number = {'BG': -1, 'BG Family': -0.9, 'BG Friend': -0.8, 'Couple': -0.8, 'Family': -0.75, 'Friend': -0.5, 'Preference': -0.25, '': 0, 'Negative Preference': 0.25, 'Apart': 1}

    num_dict = {k:rel_name_to_number[v] for k,v in name_dict.items()}

    return num_dict

'''
Function to take dictionary input and output a relationship numpy matrix
'''
    
def to_relationship_matrix(result_dict):

    result_dict = rel_name_to_number(result_dict)
    result_dict_2 = {k[::-1]: int(v) for k,v in result_dict.items()}
    null_values = {(x,x): 0 for x in range(int(((1+(np.sqrt(1+(8*len(result_dict)))))/2)))}
    result_dict_merged = result_dict | result_dict_2 | null_values
    n = np.sqrt(len(result_dict_merged)).astype(int)
    M = dok_matrix((n,n))
    M._update(result_dict_merged)

    return M.toarray().tolist()

'''
Divides the table plan into tables
'''

def plan_cutter(table_i, i):
    table_i = table_i.loc[table_i['Assigned Table No'] == i]
    table_name = "Table " + str(i)
    table_i.insert(0, table_name, range(1, len(table_i.index)+1))
    table_i.drop(columns = ["Assigned Table No"], inplace = True)
    table_i[table_name] = "Seat " + table_i[table_name].astype(str)

    return table_i

'''
Function to process the model result and make it readable
'''

def display_model(model_result, names):

    table_plan  = model_result["Table Plan"]

    multiplier_table=[]

    table_count = len(table_plan) +1 

    for i in range(1,table_count):
        multiplier_table.append([i])
        
    suggested_arrangement=pd.DataFrame(np.array(table_plan)*np.array(multiplier_table)).T

    for i in range(len(table_plan)):
        suggested_arrangement.rename(columns={i: "Table " + str(i+1)}, inplace=True)

    suggested_arrangement["Assigned Table No"]=suggested_arrangement.sum(axis=1)

    suggested_arrangement.index = names

    suggested_arrangement.rename_axis("Guest Name", inplace = True, axis=1)

    suggested_arrangement=suggested_arrangement[["Assigned Table No"]]

    suggested_arrangement_by_tableNo=suggested_arrangement.sort_values(by=['Assigned Table No'])
    suggested_arrangement_by_tableNo[["Assigned Table No"]]


    table_list = []

    for table in range(1, table_count):
        table_list.append(plan_cutter(suggested_arrangement_by_tableNo, table).to_html(classes = "\" style = \"display:inline-table; margin: 10px;\""))

    return table_list