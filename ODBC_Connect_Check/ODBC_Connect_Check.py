'''
Function: ODBC connect test
    use the Connect String to connect to the ODBC
    Check if any error.
    print the error information.
'''

import pypyodbc

# 64 bit Access DB with ODBC
# connStr = "DSN=CIS_PartLib_P_64;Uid=cadence_port;Pwd=Cadence_CIS.3;"
# connStr = "DSN=CIS_PartLib_P_64_access;"
# connStr = "DSN=AD_Sqlite3;"
# connStr = "DSN=CONNECT Partslib V2;Uid=LIMBAS2USER;Pwd=LIMBASREAD;"

# 输入ODBC DSN name
DSN_Name = input("PLease input the ODBC DSN Name(ODBC数据源名称,回车输入默认值:CIS_PartLib_P_64):\n")
if DSN_Name == "":
    DSN_Name = "CIS_PartLib_P_64"
connStr = "DSN=" + DSN_Name + ";"

print("connStr is:\t{}\n".format(connStr))

# 32 bit Access DB with ODBC, can not with in pypyodbc.
# pypyodbc.Error: ('IM014', '[IM014] [Microsoft][ODBC Driver Manager] The specified DSN contains an architecture mismatch between the Driver and Application')
# connStr = "DSN=CIS_PartLib_P_32;Uid=cadence_port;Pwd=Cadence_CIS.3;"
try:
    print("Connect to ODBC ...\n")
    conn = pypyodbc.connect(connStr)
    cursor = conn.cursor()

    print("Getting Table name ...\n")
    # 先获取所有表名
    cursor.tables(tableType="TABLE")
    table_names = cursor.fetchall()

    # 打印表名
    print("Tables inforamtion:")
    for table_name in table_names:
        print(table_name)
except Exception as e:
    print("Open ODBC error: {}".format(e))

input("按下回车键继续...")
