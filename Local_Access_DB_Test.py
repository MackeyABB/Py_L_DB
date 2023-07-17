'''
ref: 
参考这里是有问题：
https://github.com/pypyodbc/pypyodbc


需要参考以下例子：
https://github.com/jiangwen365/pypyodbc/wiki/Access-MDB-support

'''

# Microsoft Access DB
import pypyodbc 

# 创建新的*.mdb文件，有些路径显示没有权限，
# 创建了新文件之后，是不能直接使用这个connection来访问的
# connection = pypyodbc.win_create_mdb('C:\\Temp\\database.mdb')

# 必须使用以下方法连接数据库
connection = pypyodbc.win_connect_mdb('C:\\Temp\\database1.mdb')

SQL = 'CREATE TABLE saleout1 (id COUNTER PRIMARY KEY,product_name VARCHAR(25));'
# 插入数据
# SQL = "INSERT INTO saleout1 VALUES (1, 'Test1');"

# 实测显示，需要最后执行commit()才会在数据库文件中创建完成"saleout" Table
connection.cursor().execute(SQL).commit()

# connection.close()

# 以下并没有办法获取所有表的清单, 提示：no read permission on 'MSYSOBJECTS'
# SQL = 'SELECT NAME FROM MSYSOBJECTS WHERE TYPE=1 AND FLAGS=0'
# cur = connection.cursor()
# cur.execute(SQL).commit()
# result = cur.fetchall()
# print(result)

# 参见：https://stackoverflow.com/questions/11049564/pyodbc-access-database-msysobjects-permissions-issue
# 使用cursor.tables()来获取，如下
cursor = connection.cursor()
tableNames = [x[2] for x in cursor.tables().fetchall() if x[3] == 'TABLE']
print(tableNames)


connection.close()

