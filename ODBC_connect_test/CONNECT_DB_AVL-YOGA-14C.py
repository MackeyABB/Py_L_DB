'''
Function:   图形界面查询电子元器件数据库的器件信息

#todo:
1. 设置最大数据搜索数量和显示数量
2. treeview某行被选中，输出选中的内容，如双击显示所选内容（弹窗)。
3. 导出所有数据
4. Excel AVL导入，并进行数据库检索，然后输出AVL

#?
1. treeview生成的显示列表tv_display()，未找到办法与水平滚动条关联 => 参见"Func_Test\Treeview_Horizontal_Scrolbar.py"使用frame()和设置weight方法解决问题
2. treeview的宽度太大，使得其它控件的显示出现问题。=> 参见"Func_Test\Treeview_Horizontal_Scrolbar.py"使用frame()和设置weight方法解决问题


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

    def defaul(self, dbindex):
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
            # columns = [column[0] for column in cursor.description]
            columnNameList = [column[0] for column in self.cursor.description]
            sql_result = self.cursor.fetchall()
            # print(sql_result)
            return sql_result, columnNameList
        # 03-P Disk Access
        elif dbindex == 2:
            pass


# Create Global database object
# windows
master = Tk()
master.geometry("800x500")
master.title("CONNECT DB Viewer")
# master.propagate(False)

# Frame for object
frm = ttk.Frame(master)

# windows parameter
DBList = ['01-CONNECT Online(ODBC)',
          '02-Access Online(ODBC)', '03-P Disk Access']
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
    db.openDB(cmb_value, cmb_index, DBList)


def funcBtnDBDisConn():
    # BtnDBDisConn按钮的函数
    db.listTable()


def funcBtnSearch():
    # BtnSearch按钮的函数
    tableToSearch = cmb_PartType.get()
    cmb_index = cmb_DB_Select.current()
    result, columnNameList = db.fetch(tableToSearch, cmb_index)
    print(result[0])
    # 结果显示
    populate_list(result, columnNameList)


def populate_list(dataToDisplay, columnNameList):
    # 清空显示的内容
    tv_Display.delete(*tv_Display.get_children())
    # 更新表头
    colLen = len(columnNameList)
    columnNameListTuple = ()
    for columnName in columnNameList:
        columnNameListTuple = columnNameListTuple + (columnName,)
    tv_Display['columns'] = columnNameListTuple
    # 问题，为什么第一次显示不会调整宽度的？
    # 需要在修改colum参数之前刷新一下
    tv_Display.update()
    # Set column name and width
    for columnName in columnNameList:
        tv_Display.column(str(columnName), width=10, minwidth=80)
    for columnName in columnNameList:
        tv_Display.heading(columnName, text=columnName)
    # 更新显示的信息
    counter = 0
    for row in dataToDisplay:
        tv_Display.insert(parent='', index=counter, iid=counter, values=row)
        counter += 1
        # if (counter > 100):
        #     break
    # 为避免treeview的宽度太大导致其它控件显示超出范围，需要设置一下它的colunnspan
    # 依然未达到想要的效果 ==> 以下不需要重新设置，通过Frame()的方式可以解决问题了。
    # tv_Display.grid(columnspan = colLen)


# DB selection and Connection, disconnection
lbl_DB_Select = tkinter.Label(frm, text='DB Selection')

cmb_DB_Select = ttk.Combobox(frm, values=DBList)
cmb_DB_Select.set(DBList[1])

btn_DB_Connect = tkinter.Button(
    frm, text='DB Connect', command=funcBtnDBConnect)

btn_DB_DisConnect = tkinter.Button(
    frm, text='DB DisConn', command=funcBtnDBDisConn)

# part type combobox
lbl_PartType = tkinter.Label(frm, text="Part Type")
cmb_PartType = ttk.Combobox(frm, values=PartTypeList)
cmb_PartType.set(PartTypeList[1])

# Search by
lbl_SearchBy = tkinter.Label(frm, text="Search By")
# PartNo
lbl_PartNo = tkinter.Label(frm, text="PartNo")
input_PartNo = tkinter.Entry(frm, width=10)
# SAPNo
lbl_SAPNo = tkinter.Label(frm, text="SAP No")
input_SAPNo = tkinter.Entry(frm, width=10)
# PartValue
lbl_PartValue = tkinter.Label(frm, text="PartValue")
input_PartValue = tkinter.Entry(frm, width=10)


# Button
btn_Search = tkinter.Button(frm, text="Search", command=funcBtnSearch)


# Display Window
DISPLAY_ROWS = 10
TREEVIEW_COL = 6
# frm_Display = tkinter.Frame(master)
# frm_Display.grid(row=6, column=0, rowspan = 10, columnspan = 5, padx=10, pady = 10, sticky=N+S+E+W)
# ScrollBar vetical
scrb_V_Display = tkinter.Scrollbar(frm, orient='vertical')
# ScrollBar horizontal
scrb_H_Display = tkinter.Scrollbar(frm, orient='horizontal')
# Treeview to display
COLS = 20
columnRange = ()
for i in range(1, COLS):
    columnRange = columnRange + (i,)

tv_Display = ttk.Treeview(
    frm, show='headings', yscrollcommand=scrb_V_Display.set, xscrollcommand=scrb_H_Display.set)
tv_Display['columns'] = columnRange
tv_Display['height'] = DISPLAY_ROWS
# Set column name and width
for i in range(1, COLS):
    tv_Display.heading(i, text=str(i))
    tv_Display.column(i, width=50)
for line in range(0, 100):
    showdata = (line, "vineet", "e11", 1000000.00)
    tv_Display.insert(parent='', index=line, iid=line, values=showdata)
# 在Scrollbar中，绑定Scrollbar和List
scrb_V_Display.configure(command=tv_Display.yview)
scrb_H_Display.configure(command=tv_Display.xview)

# set position of all above objects by grid
frm.grid(row=0, column=0, sticky=(N, S, E, W))
# row 0
lbl_DB_Select.grid(row=0, column=0, padx=10, pady=10, sticky=W)
cmb_DB_Select.grid(row=0, column=1, padx=10, pady=10, sticky=W)
btn_DB_Connect.grid(row=0, column=2, padx=10, pady=10, sticky=W)
btn_DB_DisConnect.grid(row=0, column=3, padx=10, pady=10, sticky=W)
# row 1
lbl_PartType.grid(row=1, column=0, padx=10, pady=10, sticky=W)
cmb_PartType.grid(row=1, column=1, padx=10, pady=10, sticky=W)
# row 2
lbl_SearchBy.grid(row=2, column=0, padx=10, pady=10, sticky=W)
# row 3
lbl_PartNo.grid(row=3, column=0, padx=10, pady=10, sticky=W)
input_PartNo.grid(row=3, column=1, padx=10, pady=10, sticky=W)
lbl_SAPNo.grid(row=3, column=2, padx=10, pady=10, sticky=W)
input_SAPNo.grid(row=3, column=3, padx=10, pady=10, sticky=W)
lbl_PartValue.grid(row=3, column=4, padx=10, pady=10, sticky=W)
input_PartValue.grid(row=3, column=5, padx=10, pady=10, sticky=W)
# row 4
btn_Search.grid(row=4, column=0, padx=10, pady=10, sticky=W)
# row 5
# row 6
scrb_V_Display.grid(row=6, column=TREEVIEW_COL+1,
                    rowspan=DISPLAY_ROWS, padx=0, pady=10, sticky=N+S+E)
scrb_H_Display.grid(row=6+DISPLAY_ROWS, column=0, rowspan=6,
                    columnspan=TREEVIEW_COL, padx=10, pady=1, sticky=N+S+E+W)
tv_Display.grid(row=6, column=0, rowspan=DISPLAY_ROWS,
                columnspan=TREEVIEW_COL, padx=0, pady=10, sticky=W)

# tv_Display.propagate(False)
# tv_Display.rowconfigure(1, weight=1)
# tv_Display.columnconfigure(1, weight=1)

# handling resize =>解决了水平滚动条和treeview过宽的显示问题。
master.columnconfigure(0, weight=3)
master.rowconfigure(0, weight=1)
frm.columnconfigure(0, weight=1)
frm.columnconfigure(1, weight=1)
frm.columnconfigure(2, weight=1)
frm.columnconfigure(3, weight=1)
frm.columnconfigure(4, weight=1)
frm.columnconfigure(5, weight=1)
frm.columnconfigure(6, weight=1)


frm.mainloop()
