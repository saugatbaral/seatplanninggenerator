def missing(missing,st_list):
    for  i in missing:
        for j in st_list:
            if (j  == i):
                st_list.remove(i)
    return st_list

def run(el_list,sc_list,cm_list,col,row):
    el = len(el_list)
    sc = len(sc_list)
    cm = len(cm_list)
    temp_matrix =[]
    while ( cm_list != [] or el_list != [] or sc_list != [] ):
        if (cm == sc == el):
            temp_matrix.append(sc_list[:1])    
            sc_list = sc_list[1:]
            temp_matrix.append(el_list[:1])
            el_list = el_list[1:]
            temp_matrix.append(cm_list[:1])
            cm_list = cm_list[1:]
        elif(el >= sc) and (el > cm):
            if(sc > cm ):
                if (cm_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]     
                    temp_matrix.append(sc_list[:1])    
                    sc_list = sc_list[1:]
                    temp_matrix.append(cm_list[:1])
                    cm_list = cm_list[1:]        
                elif(sc_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(sc_list[:1])    
                    sc_list = sc_list[1:]
                elif(el_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(cm_list[:1])
                    cm_list = cm_list[1:]
            elif(cm > sc):
                if (sc_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]     
                    temp_matrix.append(sc_list[:1])    
                    sc_list = sc_list[1:]
                    temp_matrix.append(cm_list[:1])
                    cm_list = cm_list[1:]        
                elif(cm_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(cm_list[:1])
                    cm_list = cm_list[1:]
                elif(el_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(sc_list[:1])    
                    sc_list = sc_list[1:]
        elif(sc >= cm) and (sc > el):
            if(el > cm):
                if (cm_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]     
                    temp_matrix.append(sc_list[:1])    
                    sc_list = sc_list[1:]
                    temp_matrix.append(cm_list[:1])
                    cm_list = cm_list[1:] 
                elif(el_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(sc_list[:1])    
                    sc_list = sc_list[1:]
                elif(sc_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(sc_list[:1])    
                    sc_list = sc_list[1:]
            elif(cm > el ):
                if (el_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]     
                    temp_matrix.append(sc_list[:1])    
                    sc_list = sc_list[1:]
                    temp_matrix.append(cm_list[:1])
                    cm_list = cm_list[1:] 
                elif(cm_list != []):
                    temp_matrix.append(cm_list[:1])
                    cm_list = cm_list[1:]
                    temp_matrix.append(sc_list[:1])    
                    sc_list = sc_list[1:]
                elif(sc_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(sc_list[:1])    
                    sc_list = sc_list[1:]
        elif(cm >= el) and (cm > sc):
            if(sc > el):
                if (el_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]     
                    temp_matrix.append(sc_list[:1])    
                    sc_list = sc_list[1:]
                    temp_matrix.append(cm_list[:1])
                    cm_list = cm_list[1:] 
                elif(sc_list != []):
                    temp_matrix.append(sc_list[:1])    
                    sc_list = sc_list[1:]
                    temp_matrix.append(cm_list[:1])
                    cm_list = cm_list[1:]
                elif(cm_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(cm_list[:1])
                    cm_list = cm_list[1:]
                    
            elif( el > sc):
                if (sc_list != []):
                    temp_matrix.append(cm_list[:1])
                    cm_list = cm_list[1:] 
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]     
                    temp_matrix.append(sc_list[:1])    
                    sc_list = sc_list[1:]
                    
                elif(el_list != []):
                    temp_matrix.append(cm_list[:1])
                    cm_list = cm_list[1:]
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                elif(cm_list != []):
                    temp_matrix.append(cm_list[:1])
                    cm_list = cm_list[1:]
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    
                   
    matrix= [] 
    for i in range(row):# A for loop for row entries 
        a =[]
        for j in range(col):# A for loop for column entries
            b = temp_matrix[:1]
            b =str(b)[1:-1]
           # b= str(b)[1:-1]
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
def write(result,room_no):
    data = result
    writer = pd.ExcelWriter('static/excel/'+room_no+'.xlsx', engine='xlsxwriter')
    df = pd.DataFrame(data)
    df.to_excel(writer, sheet_name=room_no,header=None,index=False)
    writer.save()

def read(room_no):
    temp = pd.read_excel('static/excel/'+room_no+'.xlsx',header=None,index_col=False).astype(str)
    return temp



 