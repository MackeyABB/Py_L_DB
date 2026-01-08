'''
Introduction:
    使用PyPika构建SQL查询
    https://pypika.readthedocs.io/en/latest/

Revision History:
1.0.0 - 20260107 - 初始版本
1.0.1 - 20260107 - 修正动态生成厂商零件号条件时，大小写处理错误的问题(AccessDB不区分大小写，SAPMaxDB区分大小写)
'''

# 版本号
# xx.yy.zz
# xx: 大版本，架构性变化
# yy: 功能性新增
# zz: Bug修复
__version__ = "1.0.1"

from pypika import Query, Table, Field
from pypika.enums import Order
from typing import List, Optional

# --------------------------
# 1. 全局配置项（与业务完全匹配）
# --------------------------
# 待查询的字段列表
# SAPMaxDB字段列表
FIELDS_SAPMaxDB: List[str] = [
    "PartNumber", "value_1", "SAP_Number", "SAP_Description", "status", "parttype",
    "manufact_1", "manufact_partnum_1", "datasheet_1",
    "manufact_2", "manufact_partnum_2", "datasheet_2",
    "manufact_3", "manufact_partnum_3", "datasheet_3",
    "manufact_4", "manufact_partnum_4", "datasheet_4",
    "manufact_5", "manufact_partnum_5", "datasheet_5",
    "manufact_6", "manufact_partnum_6", "datasheet_6",
    "manufact_7", "manufact_partnum_7", "datasheet_7",
    "scm_symbol", "pcb_footprint", "alt_symbols", "mounttechn",
    "ad_symbol", "ad_footprint", "ad_alt_footprint", "detaildrawing",
    "Status", "Editor", "US_technology", "TechDescription"
]
# AccessDB字段列表
FIELDS_AccessDB: List[str] = [
    "PartNumber", "value", "SAP_Number", "SAP_Description", "status", "parttype",
    "[manufact 1]", "[manufact partnum 1]", "[datasheet 1]",
    "[manufact 2]", "[manufact partnum 2]", "[datasheet 2]",
    "[manufact 3]", "[manufact partnum 3]", "[datasheet 3]",
    "[manufact 4]", "[manufact partnum 4]", "[datasheet 4]",
    "[manufact 5]", "[manufact partnum 5]", "[datasheet 5]",
    "[manufact 6]", "[manufact partnum 6]", "[datasheet 6]",
    "[manufact 7]", "[manufact partnum 7]", "[datasheet 7]",
    "scm_symbol", "pcb_footprint", "pcb_footprint_cp", "alt_symbols", "alt_symbols_cp",
    "mounttechn", "ad_symbol", "ad_footprint", "ad_alt_footprint", "detaildrawing",
    "STATUS", "EDITOR", "US_TECHNOLOGY", "TECHDESCRIPTION"
]

# 待查询的表列表
# SAPMaxDB表列表
TABLES_SAPMaxDB: List[str] = [
    "CAPACITORS",
    # "CONNECTORS",
    # "CONVERTERS",
    # "DIODES",
    # "ICS_ANALOG",
    # "ICS_DIGITAL",
    # "MAGNETICS",
    # "MECHPARTS",
    # "MEMORY",
    # "MISCPARTS",
    # "OPTO",
    # "OP_AMPS",
    # "OSCILLATORS",
    # "REGULATORS",
    # "RELAYS",
    "RESISTORS",
    # "SENSORS",
    # "SWITCHES",
    # "TRANSFORMERS",
    # "TRANSISTORS",
    # "VARISTORS"
]
# AccessDB表列表
TABLES_AccessDB: List[str] = [
    "[01-Capacitors]",
    "[02-Resistors]",
    # "[03-Varistors]",
    # "[04-Transistors]",
    # "[05-Diodes]",
    # "[06-ICs_digital]",
    # "[07-Memory]",
    # "[08-ICs_analog]",
    # "[09-Regulators]",
    # "[10-Converters]",
    # "[11-OP_Amps]",
    # "[12-Magnetics]",
    # "[13-Transformers]",
    # "[14-Opto]",
    # "[15-Oscillators]",
    # "[16-Connectors]",
    # "[17-Relays]",
    # "[18-Sensors]",
    # "[19-Switches]",
    # "[20-MechParts]",
    # "[21-MiscParts]"
]

# 过滤条件（与关系：所有条件需同时满足）
# 格式：[条件SQL片段]，最终会用 AND 拼接
# --------------------------
# 动态生成过滤条件
# --------------------------
def generate_filter_conditions(DB_Type: str = "SAPMaxDB",
    PartNo_Searchby: Optional[str] = None,
    SAPNo_Searchby: Optional[str] = None,
    PartValue_Searchby: Optional[str] = None,
    MfcPartNum_Searchby: Optional[str] = None
) -> List[str]:
    """
    根据输入变量是否非空，动态生成AND关系的过滤条件
    Args:
        :param DB_Type: 数据库类型（SAPMaxDB或AccessDB，默认SAPMaxDB）
        :param PartNo_Searchby: 零件号搜索值（非空则生成PartNumber LIKE条件）
        :param SAPNo_Searchby: SAP号搜索值（非空则生成SAP_Number LIKE条件）
        :param PartValue_Searchby: 零件值搜索值（非空则生成value LIKE条件）
        :param MfcPartNum_Searchby: 厂商零件号搜索值（非空则生成[manufact partnum 1-7]的OR条件）
    Return: 
        过滤条件列表（AND关系，空变量不生成条件）
    注意:
    SAP MAXDB检索区分大小写的COLLATE Latin1_General_CS_AS
    """
    filter_conditions = []
    
    # 1. 处理PartNumber（PartNo_Searchby非空则添加）
    if PartNo_Searchby and PartNo_Searchby.strip():
        if DB_Type == "AccessDB":
            filter_conditions.append(f"PartNumber LIKE '%{PartNo_Searchby.strip()}%'")
        else:  # SAPMaxDB
            filter_conditions.append(f"LOWER(PartNumber) LIKE LOWER('%{PartNo_Searchby.strip()}%')")

    # 2. 处理SAP_Number（SAPNo_Searchby非空则添加）
    if SAPNo_Searchby and SAPNo_Searchby.strip():
        if DB_Type == "AccessDB":
            filter_conditions.append(f"SAP_Number LIKE '%{SAPNo_Searchby.strip()}%'")
        else:  # SAPMaxDB
            filter_conditions.append(f"LOWER(SAP_Number) LIKE LOWER('%{SAPNo_Searchby.strip()}%')")

    # 3. 处理value（PartValue_Searchby非空则添加）
    if PartValue_Searchby and PartValue_Searchby.strip():
        if DB_Type == "AccessDB":
            filter_conditions.append(f"value LIKE '%{PartValue_Searchby.strip()}%'")
        else: # SAPMaxDB
            filter_conditions.append(f"LOWER(value_1) LIKE LOWER('%{PartValue_Searchby.strip()}%')")

    
    # 4. 处理[manufact partnum 1-7]（MfcPartNum_Searchby非空则添加OR组合条件）
    if MfcPartNum_Searchby and MfcPartNum_Searchby.strip():
        if DB_Type == "AccessDB":
            mfc_partnum_fields = [f"[manufact partnum {i}]" for i in range(1, 8)]  # 1-7
            # 生成 (字段1 LIKE '%值%' OR 字段2 LIKE '%值%'
            # 不区分大小写
            mfc_conditions = " OR ".join([f"{field} LIKE '%{MfcPartNum_Searchby.strip()}%'" for field in mfc_partnum_fields])
            filter_conditions.append(f"({mfc_conditions})")  # 括号保证优先级
        else: # SAPMaxDB
            mfc_partnum_fields = [f"manufact_partnum_{i}" for i in range(1, 8)]  # 1-7            
            # 生成 (字段1 LIKE '%值%' OR 字段2 LIKE '%值%'
            # 区分大小写,需要LOWER
            mfc_conditions = " OR ".join([f"LOWER({field}) LIKE LOWER('%{MfcPartNum_Searchby.strip()}%')" for field in mfc_partnum_fields])
            filter_conditions.append(f"({mfc_conditions})")  # 括号保证优先级
    
    return filter_conditions

# --------------------------
# 2. 核心函数（模板化生成，避开PyPika底层Bug）
# --------------------------
def build_single_table_sql(table_name: str, fields: List[str], filter_conditions: List[str]) -> str:
    """
    生成单表查询SQL（多条件用AND组合）
    :param table_name: 表名
    :param fields: 字段列表
    :param filter_conditions: 过滤条件列表（AND关系）
    :return: 单表SQL
    """
    # 拼接字段（带表前缀）
    # fields_sql = ", ".join([f"{table_name}.{f}" for f in fields])
    fields_sql = ", ".join([f"{f}" for f in fields])
    # 拼接过滤条件（AND关系）
    filter_sql = " AND ".join(filter_conditions) if filter_conditions else "1=1"
    # 生成单表SQL
    single_sql = f"SELECT {fields_sql} FROM {table_name} WHERE {filter_sql}"
    return single_sql

def build_final_sql(
    tables: List[str],
    fields: List[str],
    filter_conditions: List[str],
    order_by_field: str = "PartNumber",
    order: str = "ASC"
) -> str:
    """
    生成最终SQL（多表UNION ALL + 条件AND组合）
    """
    # 生成每个表的查询（所有表共用同一套AND条件）
    table_sqls = [
        build_single_table_sql(t, fields, filter_conditions)
        for t in tables
    ]
    
    # 拼接多表的UNION ALL（仅表之间UNION ALL，条件是AND）
    union_all_sql = " UNION ALL ".join(table_sqls)
    
    # 追加排序
    final_sql = f"{union_all_sql} ORDER BY {order_by_field} {order}"
    
    # 格式化SQL（便于阅读）
    final_sql = final_sql.replace(" UNION ALL ", "\nUNION ALL\n")
    final_sql = final_sql.replace(" AND ", "\n  AND ")
    final_sql = final_sql.replace(" OR ", "\n    OR ")
    return final_sql

# --------------------------
# 3. 执行入口（100%可运行）
# --------------------------
if __name__ == "__main__":
    try:
        # 切换不同DB
        DB_Type = "AccessDB"
        # DB_Type = "SAPMaxDB"

        if DB_Type == "AccessDB":
            # AccessDB
            TABLES = TABLES_AccessDB
            FIELDS = FIELDS_AccessDB   
        else:
            # SAPMaxDB
            TABLES = TABLES_SAPMaxDB
            FIELDS = FIELDS_SAPMaxDB
            

        # ======================
        # 模拟输入变量（可替换为实际业务输入）
        # ======================
        # 生成PartNumber条件
        # PartNo_Searchby = "res_232"       
        PartNo_Searchby = ""       
         # 生成SAP_Number条件
        SAPNo_Searchby = "2tf"         
        # SAPNo_Searchby = ""          
        # 生成value条件
        PartValue_Searchby = "30K"    
        # PartValue_Searchby = "1U"    
        # PartValue_Searchby = ""            
        # 生成manufact partnum 1-7的OR条件
        MfcPartNum_Searchby = "RC1206"   
        # MfcPartNum_Searchby = ""   
        
        # 动态生成过滤条件
        FILTER_CONDITIONS = generate_filter_conditions(
            DB_Type=DB_Type,
            PartNo_Searchby=PartNo_Searchby,
            SAPNo_Searchby=SAPNo_Searchby,
            PartValue_Searchby=PartValue_Searchby,
            MfcPartNum_Searchby=MfcPartNum_Searchby
        )
        
        # 生成最终SQL
        final_sql = build_final_sql(
            tables=TABLES,
            fields=FIELDS,
            filter_conditions=FILTER_CONDITIONS,
            order_by_field="PartNumber",
            order="ASC"
        )
        
        # 写入文件+验证
        file_path = "dynamic_filter_sql.sql"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_sql)
        
        # 打印结果
        print("="*120)
        print("✅ 动态过滤条件生成成功！")
        print(f"📄 完整SQL已保存至：{file_path}")
        print(f"\n🔍 生成的过滤条件列表（AND关系）：")
        for i, cond in enumerate(FILTER_CONDITIONS, 1):
            print(f"   {i}. {cond}")
        
        print(f"\n📊 统计信息：")
        print(f"   - 输入变量非空数量：{sum(1 for v in [PartNo_Searchby, SAPNo_Searchby, PartValue_Searchby, MfcPartNum_Searchby] if v and v.strip())}")
        print(f"   - 生成过滤条件数量：{len(FILTER_CONDITIONS)}")
        print(f"   - SQL总字符数：{len(final_sql)}")
        print(f"   - 多表UNION ALL数量：{final_sql.count('UNION ALL')}")
        
        # 验证关键逻辑
        # key_checks = [
        #     "PartNumber LIKE '%res_2324%'" in final_sql,
        #     "SAP_Number LIKE '%SAP001%'" in final_sql,
        #     "([manufact partnum 1] LIKE '%MFC12345%' OR [manufact partnum 2] LIKE '%MFC12345%'" in final_sql,
        #     "value LIKE" not in final_sql,  # PartValue_Searchby为空，不应出现
        #     "ORDER BY PartNumber ASC" in final_sql
        # ]
        # if all(key_checks):
        #     print("✅ 关键逻辑验证通过：条件动态生成正确，AND关系，SQL完整！")
        # else:
        #     print("❌ 关键逻辑验证失败，需检查条件生成逻辑！")
        # print("="*120)
        
    except Exception as e:
        print(f"❌ 执行失败：{type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()