# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 11:35:02 2020

@author: CNMALAO

Function:
    遍历数据库所有数据，
    将SAP_Number以“2TF"开头的数据输出到excel中。

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

# create the SQL query
sql_query_list = []
for table_name in table_list:
    sql_query_list.append("SELECT PartNumber, SAP_Number, AD_Symbol,PCB_Footprint, Alt_Symbols from [" + table_name + r"] where SAP_Number like '2TF%'")

# 写入表头
col_name = ["PartNumber", "SAP_Number", "AD_Symbol", "PCB_Footprint", "Alt_Symbols"]
# create new file
wb = xlwt.Workbook()
ws = wb.add_sheet('PartList')
cols = len(col_name)
excel_row_num = 0
for i in range(0,cols-1):
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
            for i in range(0,cols-1):
                ws.write(excel_row_num,i,row[i])
            excel_row_num += 1
    print(f"===Finish===={sql_search}")
    
wb.save("List.xls")