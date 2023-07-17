'''
https://stackoverflow.com/questions/12704305/return-column-names-from-pyodbc-execute-statement
'''

import pypyodbc

# 64 bit Access DB with ODBC
# connStr = "DSN=CIS_PartLib_P_64;Uid=cadence_port;Pwd=Cadence_CIS.3;"
# connStr = "DSN=CIS_PartLib_P_64_access;"
# connStr = "DSN=AD_Sqlite3;"

# 输入ODBC DSN name
DSN_Name = input("PLease input the ODBC DSN Name(ODBC数据源名称,回车输入默认值:CIS_PartLib_P_64):\n")
if DSN_Name == "":
    DSN_Name = "CIS_PartLib_P_64"
connStr = "DSN=" + DSN_Name + ";"

print("connStr is:\t{}\n".format(connStr))

# 32 bit Access DB with ODBC, can not with in pypyodbc.
# pypyodbc.Error: ('IM014', '[IM014] [Microsoft][ODBC Driver Manager] The specified DSN contains an architecture mismatch between the Driver and Application')
# connStr = "DSN=CIS_PartLib_P_32;Uid=cadence_port;Pwd=Cadence_CIS.3;"
conn = pypyodbc.connect(connStr)
cursor = conn.cursor()


# 先获取所有表名
cursor.tables(tableType="TABLE")
table_names = cursor.fetchall()

# 打印表名
print("Tables inforamtion:")
for table_name in table_names:
    print(table_name)

input("按下回车键继续...")

# 下面的方法不可行：
# for row in cursor.columns(table='01-Capacitors'):
#     print(row.column_name)

print("\n输出表01-Capacitors的列名:")
# 这个获取可能是系统表的field
cursor.columns(table='01-Capacitors')
columns = [column[0] for column in cursor.description]
print(columns)

print("\n输出表01-Capacitors的数据清单的头:")
# 尝试先执行SQL命令后，再获取column名称，可行
sql = "SELECT * FROM [01-Capacitors];"
cursor.execute(sql)
columns = [column[0] for column in cursor.description]
print(columns)

conn.close()

input("按下回车键退出...")