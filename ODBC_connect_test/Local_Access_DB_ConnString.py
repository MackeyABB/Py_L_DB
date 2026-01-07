'''
https://www.connectionstrings.com/access/

出错，无法直接访问*.mdb文件
pypyodbc.Error: ('IM002', '[IM002] [Microsoft][ODBC Driver Manager] Data source name not found and no default driver specified')

这是因为
使用的驱动是32位，如下：
Driver={Microsoft Access Driver (*.mdb)}

pyodbc只支持64位驱动，需要使用
Microsoft Access Driver (*.mdb, *.accdb)

'''



import pypyodbc

# connStr = "Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=C:\Temp\Database1.mdb;"
# connStr = "Driver={Microsoft Access Driver (*.mdb)};Dbq=C:\Temp\Database1.mdb;"
connStr = r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=P:\Cadence\CIS_DB_OL\CIS_PartLib.mdb;SystemDB=P:\Cadence\CIS_DB_OL\CIS_PartLib.mdw;Uid=cadence_port;Pwd=Cadence_CIS.3;"
# connStr = r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=D:\80_MackeyDoc\01_ABB\OneDrive - ABB\02_ABB_Work\WorkStation\90_temp\CIS_DB_OL\CIS_PartLib.mdb;SystemDB=D:\80_MackeyDoc\01_ABB\OneDrive - ABB\02_ABB_Work\WorkStation\90_temp\CIS_DB_OL\CIS_PartLib.mdw;Uid=cadence_port;Pwd=Cadence_CIS.3;"


conn = pypyodbc.connect(connStr)
cursor = conn.cursor()

# SQL = 'CREATE TABLE [saleout] (id COUNTER PRIMARY KEY,product_name VARCHAR(25));'
# SQL = 'SELECT * FROM [saleout];'
SQL = 'SELECT NAME FROM MSYSOBJECTS WHERE TYPE=1 AND FLAGS=0'

cursor.execute(SQL)
result = cursor.fetchall()
print(result)

conn.close()

