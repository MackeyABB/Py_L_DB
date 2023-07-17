# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 11:35:02 2020

@author: CNMALAO

Function:
    读取外部文件"MountTechn_List.txt"，获取PartNumber，
    然后检索数据库获取所需的Field值，并输出保存到Excel文件

    这里的Field值可以快速进行设置，方便调整输出的数据。

    以下程序可以作为：根据PartNumber等字段来检索数据库并输出所需数据的模板。

"""


import pypyodbc
import xlwt

connStr = "DSN=CIS_PartLib_P_64;Uid=cadence_port;Pwd=Cadence_CIS.3;"
conn = pypyodbc.connect(connStr)
cursor = conn.cursor()

# get the table list
sql_listTable = "SELECT NAME FROM MSYSOBJECTS WHERE TYPE=1 AND FLAGS=0"
cursor.execute(sql_listTable)
table_list = cursor.fetchall()

table_list = [('01-Capacitors'),
 ('02-Resistors'),
 ('03-Varistors'),
 ('04-Transistors'),
 ('05-Diodes'),
 ('06-ICs_digital'),
 ('07-Memory'),
 ('08-ICs_analog'),
 ('09-Regulators'),
 ('10-Converters'),
 ('11-OP_Amps'),
 ('12-Magnetics'),
 ('13-Transformers'),
 ('14-Opto'),
 ('15-Oscillators'),
 ('16-Connectors'),
 ('17-Relays'),
 ('18-Sensors'),
 ('19-Switches'),
 ('20-MechParts'),
 ('21-MiscParts')
]

# get the PartNumber from the list file
ListFileName = "MountTechn_List.txt"
PartNumberSearchList = []
with open(ListFileName,'r') as f:
    txt = f.readlines()
    for line in range(1,len(txt)):
        num = txt[line].split("\t")[0]
        PartNumberSearchList.append(num)
    print("PartNumber Search List data OK.")

# create the SQL query
# 这里设置需要输出的Field
select_list = ["PartNumber", 
                "SAP_Number", 
                "AD_Symbol", 
                "PCB_Footprint", 
                "Alt_Symbols", 
                "AD_Symbol", 
                "AD_Footprint", 
                "MountTechn",
                "TechDescription"
                ]
select_list_qurey = ",".join(select_list)
# 不管PartNumber是属于哪个Table，不作判断，省编程时间
sql_query_list = []
for table_name in table_list:
    for condition in PartNumberSearchList:
        # sql_query_list.append("SELECT PartNumber, SAP_Number, AD_Symbol,PCB_Footprint, Alt_Symbols, MountTechn from [" + table_name + r"] where PartNumber = " + condition )

        sql_query = "SELECT {select_list_qurey} from [{table_name}] where PartNumber = '{condition}'".format(select_list_qurey= select_list_qurey, table_name= table_name, condition=condition)
        sql_query_list.append(sql_query)

# 写入表头
col_name = select_list
# create new file
wb = xlwt.Workbook()
ws = wb.add_sheet('PartList')
cols = len(col_name)
excel_row_num = 0
for i in range(0,cols):
    ws.write(excel_row_num, i, col_name[i])
# wb.save("List.xls")
excel_row_num = 1
    
for sql_search in sql_query_list:
    print(f"===Start===={sql_search}")
    cursor.execute(sql_search)
    rows = cursor.fetchall()
    if not rows:
        print(f"xxxx No Data xxxx")
        continue
    else:
        for row in rows:
            for i in range(0,cols):
                ws.write(excel_row_num,i,row[i])
            excel_row_num += 1
    print(f"===Finish===={sql_search}")
    
wb.save("LookForList_Export.xls")