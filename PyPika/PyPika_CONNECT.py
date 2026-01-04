'''
Introduction:
    使用PyPika构建SQL查询
'''

from pypika import Query, Table, Field
from pypika.enums import Order
from typing import List, Callable

# --------------------------
# 1. 全局配置项（与业务完全匹配）
# --------------------------
FIELDS: List[str] = [
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

TABLES: List[str] = [
    # "[21-MiscParts]", "[20-MechParts]", "[19-Switches]", "[18-Sensors]", "[17-Relays]",
    # "[16-Connectors]", "[15-Oscillators]", "[14-Opto]", "[13-Transformers]", "[12-Magnetics]",
    # "[11-OP_Amps]", "[10-Converters]", "[09-Regulators]", "[08-ICs_analog]", "[07-Memory]",
    # "[06-ICs_digital]", "[05-Diodes]", "[04-Transistors]", "[03-Varistors]", 
    "[02-Resistors]",
    "[01-Capacitors]"
]

# 过滤条件配置（格式：(条件描述, 条件SQL片段)）
FILTER_CONDITIONS: List[tuple[str, str]] = [
    ("partnumber_filter", "PartNumber LIKE '%res_2324%'"),
    ("sapnumber_filter", "SAP_Number LIKE '%2TF%'"),
    # ("status_filter", "status = 'active'"),
]

# --------------------------
# 2. 核心函数（模板化生成，避开PyPika底层Bug）
# --------------------------
def build_single_table_sql(table_name: str, fields: List[str], filter_sql: str) -> str:
    """
    生成单表单条件的SQL片段（纯字符串拼接，避开PyPika解析）
    :param table_name: 表名（如"[21-MiscParts]"）
    :param fields: 字段列表
    :param filter_sql: 过滤条件SQL（如"PartNumber LIKE '%res_2324%'"）
    :return: 单表查询SQL
    """
    # 拼接字段（带表前缀）
    fields_sql = ", ".join([f"{f}" for f in fields])
    # 生成单表SQL
    single_sql = f"SELECT {fields_sql} FROM {table_name} WHERE {filter_sql}"
    return single_sql

def build_condition_union_sql(tables: List[str], fields: List[str], filter_sql: str) -> str:
    """生成单个条件的多表UNION ALL SQL"""
    # 生成所有单表SQL
    table_sqls = [build_single_table_sql(t, fields, filter_sql) for t in tables]
    # 拼接UNION ALL
    return " UNION ALL ".join(table_sqls)

def build_final_sql(
    tables: List[str],
    fields: List[str],
    filter_conditions: List[tuple[str, str]],
    order_by_field: str = "PartNumber",
    order: str = "ASC"
) -> str:
    """生成最终的多条件合并SQL"""
    # 生成每个条件的UNION ALL块
    condition_sql_blocks = [
        build_condition_union_sql(tables, fields, filter_sql)
        for _, filter_sql in filter_conditions
    ]
    
    # 拼接所有条件块
    union_all_sql = " UNION ALL ".join(condition_sql_blocks)
    
    # 追加排序
    final_sql = f"{union_all_sql} ORDER BY {order_by_field} {order}"
    
    # 格式化SQL（可选，便于阅读）
    final_sql = final_sql.replace(" UNION ALL ", "\nUNION ALL\n")
    final_sql = final_sql.replace(" ORDER BY ", "\nORDER BY ")
    
    return final_sql

# --------------------------
# 3. 执行入口（100%可运行）
# --------------------------
if __name__ == "__main__":
    try:
        # 生成最终SQL
        final_sql = build_final_sql(
            tables=TABLES,
            fields=FIELDS,
            filter_conditions=FILTER_CONDITIONS,
            order_by_field="PartNumber",
            order="ASC"
        )
        
        # 输出结果
        print("✅ SQL生成成功！")
        print("="*120)
        print(final_sql)
        print("="*120)

        # 1. 打印字符总数（对比预期）
        print(f"SQL总字符数：{len(final_sql)}")

        # 2. 检查关键片段是否存在（比如最后一个表、排序语句）
        if "[01-Capacitors]" in final_sql and "ORDER BY PartNumber ASC" in final_sql:
            print("✅ SQL包含所有关键内容，未截断")
        else:
            print("❌ SQL缺失关键内容，需检查生成逻辑")
        
        # 可选：将SQL写入文件（便于直接使用）
        with open("generated_sql.sql", "w", encoding="utf-8") as f:
            f.write(final_sql)
        print("📄 SQL已写入 generated_sql.sql 文件")
        
    except Exception as e:
        print(f"❌ SQL生成失败：{type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()