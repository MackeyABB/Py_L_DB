'''
Function: ODBC connect test
    use the Connect String to connect to the ODBC
    Check if any error.
    print the error information.
    显示“连接”和“获取表名”的时间花费。
'''

import pypyodbc
import time

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
    # Connect
    print("Connect to ODBC ...")
    start_time = time.perf_counter()
    conn = pypyodbc.connect(connStr)
    cursor = conn.cursor()
    line1_time = time.perf_counter()
    line1_execution_time = line1_time - start_time
    print(f"执行Connect的时间：{line1_execution_time}秒\n")

    # 先获取所有表名
    print("Getting Table name ...")
    line2_time = time.perf_counter()
    cursor.tables(tableType="TABLE")
    table_names = cursor.fetchall()
    line3_time = time.perf_counter()
    line3_execution_time = line3_time - line2_time
    print(f"执行获取表名的时间：{line3_execution_time}秒\n")

    # 打印表名
    print("Tables inforamtion:")
    for table_name in table_names:
        print(table_name)
    
    # 打印正常信息
    print("\033[1;31;40m打开ODBC数据库正常！滚动窗口显示全部信息。\033[0m")

except Exception as e:
    print("\033[1;31;40m Open ODBC error: {} \033[0m".format(e))

input("按下回车键继续...")
