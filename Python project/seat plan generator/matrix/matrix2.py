def missing(missing,st_list):
    for  i in missing:
        for j in st_list:
            if (j  == i):
                st_list.remove(i)
    return st_list

def run(el_list,sc_list,cm_list,col,row): 

    temp_matrix =[]
    while ( cm_list != [] or el_list != [] or sc_list != [] ):
        temp_matrix.append(sc_list[:1])    
        sc_list = sc_list[1:]
        temp_matrix.append(el_list[:1])
        el_list = el_list[1:]
        temp_matrix.append(cm_list[:1])
        cm_list = cm_list[1:]
                   
    matrix= [] 
    for i in range(row):# A for loop for row entries 
        a =[]
        for j in range(col):# A for loop for column entries
            b = temp_matrix[:1]
            b =str(b)[1:-1]
            b= str(b)[1:-1]
            a.append(b)
            temp_matrix = temp_matrix[1:]
        matrix.append(a)
    Result = []
    for i in range(col):
        b = []
        for j in range(row):
            b.append(0)
        Result.append(b)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            Result[j][i] = matrix[i][j]
    return Result

import pandas as pd
import numpy as np
def write(result,room_no):
    data = result
    writer = pd.ExcelWriter('static/excel/'+room_no+'.xlsx', engine='xlsxwriter')
    df = pd.DataFrame(data)
    df = df.replace(np.nan, '', regex=True)
    df.to_excel(writer, sheet_name=room_no,header=None,index=False)
    writer.close()


def read(room_no):
    pd.options.display.float_format = '{:,.0f}'.format
    temp = pd.read_excel('static/excel/'+room_no+'.xlsx',header=None,index_col=False).astype(str).replace(to_replace ="nan", value =0) 
    temp = temp.replace(to_replace =0, value ="Blank") 
    
    return temp




