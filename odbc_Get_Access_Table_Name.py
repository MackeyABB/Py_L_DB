'''
https://stackoverflow.com/questions/12704305/return-column-names-from-pyodbc-execute-statement
'''

import pypyodbc

# 64 bit Access DB with ODBC
# connStr = "DSN=CIS_PartLib_P_64;Uid=cadence_port;Pwd=Cadence_CIS.3;"
# connStr = "DSN=CIS_PartLib_P_64_access;"
connStr = "DSN=AD_Sqlite3;"


print("connStr is:\t{}\n".format(connStr))

# 32 bit Access DB with ODBC, can not with in pypyodbc.
# pypyodbc.Error: ('IM014', '[IM014] [Microsoft][ODBC Driver Manager] The specified DSN contains an architecture mismatch between the Driver and Application')
# connStr = "DSN=CIS_PartLib_P_32;Uid=cadence_port;Pwd=Cadence_CIS.3;"
conn = pypyodbc.connect(connStr)
cursor = conn.cursor()

# 下面的方法不可行：
# for row in cursor.columns(table='01-Capacitors'):
#     print(row.column_name)

# 这个获取可能是系统表的field
cursor.columns(table='01-Capacitors')
columns = [column[0] for column in cursor.description]
print(columns)

print("\nMethos2:\n")
# 尝试先执行SQL命令后，再获取column名称，可行
sql = "SELECT * FROM [01-Capacitors];"
cursor.execute(sql)
columns = [column[0] for column in cursor.description]
print(columns)