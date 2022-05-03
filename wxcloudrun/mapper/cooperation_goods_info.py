# -*- coding: utf-8 -*-
'''
@author: nixiaopan
@time: 2022/4/10 0:05
'''
from wxcloudrun.mapper.utils import get_table_column_name
from wxcloudrun.utils.SQL.DBUtils import db_utils

need_escapr_string_list = ["goods_url", "pic_path", "brand", "goods_name", "specification",
                           "selling_point", "storage_condition", "unsuitable_people", "daily_price", "lowest_price",
                           "tmall_price", "taobao_price", "other_price", "live_price", "preferential_way",
                           "delivery_company",
                           "shipping_addresses", "free_shipping", "not_shipping", "comment", "store_name"]
can_not_update_string_list = ["openid", "id"]


def insert_goods_data(cooperation_id, kwargs):
    column_name_list = get_table_column_name("cooperation_goods_info")
    sql_str = 'insert into  cooperation_goods_info set '
    for k, v in kwargs.items():
        if k in can_not_update_string_list:
            continue
        if k in column_name_list:
            if k in need_escapr_string_list:  # 如果该字段需要转义
                if v != None:
                    v = db_utils.escape_string(v)
            sql_str += '{0}="{1}",'.format(k, v)
    sql_str = '{0} cooperation_id = "{1}"'.format(sql_str, cooperation_id)
    print(sql_str)
    res, _ = db_utils.execute_single_sql(sql_str)
    return res
