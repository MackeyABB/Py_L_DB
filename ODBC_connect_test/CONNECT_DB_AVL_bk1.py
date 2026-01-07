'''
Function:   图形界面查询电子元器件数据库的器件信息

备份：
1.将listbox改为treeview之前的备份

'''

from tkinter import *
from tkinter import ttk
import tkinter
import pypyodbc




# Database control class
class Database:
    def __ini__(self):
        # 初始化不需要创建任务东西
        pass
    
    def defaul(self,dbindex):
        # template
        # 01-CONNECT Online(ODBC)
        if dbindex == 0:
            pass
        # 02-Access Online(ODBC)
        elif dbindex == 1:
            pass
        # 03-P Disk Access
        elif dbindex == 2:
            pass
    
    def openDB(self, dbname, dbindex, dblist):
        # 01-CONNECT Online(ODBC)
        if dbindex == 0:
            print(dblist[dbindex])
        # 02-Access Online(ODBC)
        elif dbindex == 1:
            connStr = "DSN=CIS_PartLib_P_64;Uid=cadence_port;Pwd=Cadence_CIS.3;"
            print(dblist[dbindex])
        # 03-P Disk Access
        elif dbindex == 2:
            print(dblist[dbindex])

        # 连接数据库
        self.conn = pypyodbc.connect(connStr)
        self.cursor = self.conn.cursor()
        print("Connect DB success!")
    
    def listTable(self):    
        # get the table list
        sql_listTable = "SELECT NAME FROM MSYSOBJECTS WHERE TYPE=1 AND FLAGS=0;"
        self.cursor.execute(sql_listTable)
        table_list = self.cursor.fetchall()
        print(table_list)
        return table_list
        

    def fetch(self, tableName, dbindex):
        # fetch data
        # 01-CONNECT Online(ODBC)
        if dbindex == 0:
            pass
        # 02-Access Online(ODBC)
        elif dbindex == 1:
            sql_fetch = "SELECT * FROM [{}];".format(tableName)
            self.cursor.execute(sql_fetch)
            sql_result = self.cursor.fetchall()
            # print(sql_result)
            return sql_result
        # 03-P Disk Access
        elif dbindex == 2:
            pass
        



# Create Global database object
# windows
master = Tk()
master.geometry("800x500")
master.title("CONNECT DB Viewer")

# windows parameter
DBList = ['01-CONNECT Online(ODBC)', '02-Access Online(ODBC)', '03-P Disk Access']
PartTypeList = [('---All----'),
('01-Capacitors'),
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
# Database relative
db = Database()

# User def
def funcBtnDBConnect():
    # BtnDBConnect按键函数
    ''' Fast test
    # cmb_value = cmb_DB_Select.get()
    cmb_index = cmb_DB_Select.current()
    # print(cmb_index)
    # 01-CONNECT Online(ODBC)
    if cmb_index == 0:
        print(cmb_index)
    # 02-Access Online(ODBC)
    elif cmb_index == 1:
        connStr = "DSN=CIS_PartLib_P_64;Uid=cadence_port;Pwd=Cadence_CIS.3;"
        print(cmb_index)
    # 03-P Disk Access
    elif cmb_index == 2:
        print(cmb_index)
    
    # 连接数据库
    conn = pypyodbc.connect(connStr)
    cursor = conn.cursor()

    # get the table list
    sql_listTable = "SELECT NAME FROM MSYSOBJECTS WHERE TYPE=1 AND FLAGS=0"
    cursor.execute(sql_listTable)
    table_list = cursor.fetchall()
    print(table_list)    
    '''
    cmb_value = cmb_DB_Select.get()
    cmb_index = cmb_DB_Select.current()
    db.openDB(cmb_value,cmb_index,DBList)


def funcBtnDBDisConn():
    # BtnDBDisConn按钮的函数
    db.listTable()

def funcBtnSearch():
    # BtnSearch按钮的函数
    tableToSearch = cmb_PartType.get()
    cmb_index = cmb_DB_Select.current()
    result = db.fetch(tableToSearch, cmb_index)
    print(result[0])
    # 结果显示到listbox
    populate_list(result)

def populate_list(dataToDisplay):
    # 更新listbox的信息
    lst_Display.delete(0,END)
    counter = 0
    for row in dataToDisplay:
        lst_Display.insert(END,row)
        counter +=1
        if (counter > 10):
            break

    


# DB selection and Connection, disconnection
lbl_DB_Select = tkinter.Label(master, text = 'DB Selection')
lbl_DB_Select.grid(row = 0, column= 0, padx = 10, pady= 10, sticky=W)

cmb_DB_Select = ttk.Combobox(master, values= DBList)
cmb_DB_Select.grid(row=0, column=1, padx = 10, pady= 10, sticky=W)
cmb_DB_Select.set(DBList[1])

btn_DB_Connect = tkinter.Button(master, text='DB Connect', command=funcBtnDBConnect)
btn_DB_Connect.grid(row=0, column=2, padx = 10, pady= 10, sticky=W)

btn_DB_DisConnect = tkinter.Button(master, text='DB DisConn', command=funcBtnDBDisConn)
btn_DB_DisConnect.grid(row=0, column=3, padx = 10, pady= 10, sticky=W)

# part type combobox
lbl_PartType = tkinter.Label(master, text="Part Type")
lbl_PartType.grid(row=1, column=0, padx=10, pady = 10, sticky=W)
cmb_PartType = ttk.Combobox(master, values= PartTypeList)
cmb_PartType.grid(row=1, column=1, padx = 10, pady= 10, sticky=W)
cmb_PartType.set(PartTypeList[1])

# Search by
lbl_SearchBy = tkinter.Label(master, text="Search By")
lbl_SearchBy.grid(row=2, column=0, padx=10, pady = 10, sticky=W)
# PartNo
lbl_PartNo = tkinter.Label(master, text="PartNo")
lbl_PartNo.grid(row=3, column=0, padx=10, pady = 10, sticky=W)
input_PartNo = tkinter.Entry(master, width=10)
input_PartNo.grid(row=3, column=1, padx=10, pady = 10, sticky=W)
# SAPNo
lbl_SAPNo = tkinter.Label(master, text="SAP No")
lbl_SAPNo.grid(row=3, column=2, padx=10, pady = 10, sticky=W)
input_SAPNo = tkinter.Entry(master, width=10)
input_SAPNo.grid(row=3, column=3, padx=10, pady = 10, sticky=W)
# PartValue
lbl_PartValue = tkinter.Label(master, text="PartValue")
lbl_PartValue.grid(row=3, column=4, padx=10, pady = 10, sticky=W)
input_PartValue = tkinter.Entry(master, width=10)
input_PartValue.grid(row=3, column=5, padx=10, pady = 10, sticky=W)

# Button
btn_Search = tkinter.Button(master, text="Search", command=funcBtnSearch)
btn_Search.grid(row=4, column=0, padx=10, pady = 10, sticky=W)


# Display Window
DISPLAY_ROWS = 10
# frm_Display = tkinter.Frame(master)
# frm_Display.grid(row=6, column=0, rowspan = 10, columnspan = 5, padx=10, pady = 10, sticky=N+S+E+W)
# ScrollBar vetical
scrb_V_Display = tkinter.Scrollbar(master)
scrb_V_Display.grid(row=6, column=5, rowspan = DISPLAY_ROWS, padx=0, pady = 10, sticky=N+S)
# ScrollBar horizontal
scrb_H_Display = tkinter.Scrollbar(master, orient='horizontal')
scrb_H_Display.grid(row=6+DISPLAY_ROWS, column=0, rowspan = 1, columnspan=5, padx=10, pady = 1, sticky=N+S+E+W)
# ListBox to display
lst_Display = tkinter.Listbox(master, yscrollcommand= scrb_V_Display.set, xscrollcommand=scrb_H_Display.set)
lst_Display.grid(row=6, column=0, rowspan = DISPLAY_ROWS, columnspan = 5, padx=10, pady = 10, sticky=N+S+E+W)
for line in range(1,100):
    lst_Display.insert(END, "===================================================================" + str(line))
# 在Scrollbar中，绑定Scrollbar和List
scrb_V_Display.config(command=lst_Display.yview)
scrb_H_Display.config(command=lst_Display.xview)



master.mainloop()


