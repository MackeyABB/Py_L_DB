# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 11:35:02 2020

@author: CNMALAO

Function:
    遍历数据库所有数据，
    将SAP_Number以“2TF"开头的数据输出到TXT文件中。

"""


import pypyodbc

# 64 bit Access DB with ODBC
connStr = "DSN=CIS_PartLib_P_64;Uid=cadence_port;Pwd=Cadence_CIS.3;"
# 32 bit Access DB with ODBC, can not with in pypyodbc.
# pypyodbc.Error: ('IM014', '[IM014] [Microsoft][ODBC Driver Manager] The specified DSN contains an architecture mismatch between the Driver and Application')
# connStr = "DSN=CIS_PartLib_P_32;Uid=cadence_port;Pwd=Cadence_CIS.3;"
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
with open('list.txt','w+') as f:
    col_str = ""
    for name in col_name:
        col_str += name + '\t'
    col_str += '\n'
    f.write(col_str)
    
for sql_search in sql_query_list:
    print(f"===Start===={sql_search}")
    cursor.execute(sql_search)
    rows = cursor.fetchall()
    if not rows:
        print(f"xxxx No Data xxxx")
        continue
    else:
        with open('list.txt','a+') as f:
            for row in rows:
                f.write(str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\t' + str(row[3]) + '\t' + str(row[4])+ '\n')
    print(f"===Finish===={sql_search}")
    
