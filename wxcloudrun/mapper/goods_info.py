# -*- coding: utf-8 -*-
'''
@author: nixiaopan
@time: 2022/4/9 18:31
'''
from wxcloudrun.mapper.utils import get_table_column_name
from wxcloudrun.utils.SQL.DBUtils import db_utils

need_escapr_string_list = ["goods_name", "specification", "brand", "favorable_rate", "pic_path",
                           "live_recording_screen_path", "daily_price", "live_price",
                           "preferential_way", "goods_url", "hand_card", "tmall_price", "taobao_price", "jd_price",
                           "pdd_price", "offline_price", "storage_condition", "shelf_life", "unsuitable_people",
                           "shipping_cycle", "shipping_addresses", "delivery_company", "not_shipping",
                           "free_shipping", "comment"]

can_not_update_string_list = ["openid", "id"]


def insert_goods_data(openid, kwargs):
    column_name_list = get_table_column_name("goods_info")
    sql_str = 'insert into  goods_info set '
    for k, v in kwargs.items():
        if k in can_not_update_string_list:
            continue
        if k in column_name_list:
            if k in need_escapr_string_list:  # 如果该字段需要转义
                if k == "pic_path":
                    v = ",".join(v)
                if v != None:
                    v = db_utils.escape_string(v)
            sql_str += '{0}="{1}",'.format(k, v)
    sql_str = '{0} openid = "{1}"'.format(sql_str, openid)
    print(sql_str)
    res, pk = db_utils.execute_insert_sql_and_get_primary_key(sql_str)
    return res, pk


def update_goods_data_by_id(openid, goods_id, kwargs):
    column_name_list = get_table_column_name("goods_info")
    sql_str = 'update goods_info set '
    for k, v in kwargs.items():
        if k in can_not_update_string_list:
            continue
        if k in column_name_list:
            if k in need_escapr_string_list:  # 如果该字段需要转义
                if k == "pic_path":
                    v = ",".join(v)
                if v != None:
                    v = db_utils.escape_string(v)
            sql_str += '{0}="{1}",'.format(k, v)
    sql_str = '{0} where openid = "{1}" and id = "{2}" '.format(sql_str[:-1], openid, goods_id)
    print(sql_str)
    res, _ = db_utils.execute_single_sql(sql_str)
    return res


def get_goods_data(openid, goods_id):
    sql = """
    select * from goods_info where openid = "{openid}"  {goods_filter}
    """.format(openid=openid, goods_filter=" and id = {0}".format(goods_id) if goods_id else "")
    print(sql)
    return db_utils.execute_single_sql(sql)


def get_store_goods_data(openid, store_id):
    sql = """
    select * from goods_info where openid = "{openid}"  and store_id = "{store_id}"
    """.format(openid=openid, store_id=store_id)
    return db_utils.execute_single_sql(sql)
