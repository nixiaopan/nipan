# -*- coding: utf-8 -*-
'''
@author: nixiaopan
@time: 2022/4/9 18:31
'''
from wxcloudrun.mapper.utils import get_table_column_name
from wxcloudrun.utils.SQL.DBUtils import db_utils

need_escapr_string_list=["goods_url","pic_path","brand","goods_name","specification",
                        "selling_point","storage_condition","unsuitable_people", "daily_price","lowest_price",
                         "tmall_price","taobao_price","other_price","live_price", "preferential_way","delivery_company",
                         "shipping_addresses","free_shipping","not_shipping","comment"]
can_not_update_string_list = ["openid","id"]


def insert_goods_data(openid, kwargs):
    column_name_list = get_table_column_name("goods_info")
    sql_str = 'insert into  goods_info set '
    for k, v in kwargs.items():
        if k in can_not_update_string_list:
            continue
        if k in column_name_list:
            if k in need_escapr_string_list:  # 如果该字段需要转义
                if v != None:
                    v = db_utils.escape_string(v)
            sql_str += '{0}="{1}",'.format(k, v)
    sql_str = '{0} openid = "{1}"'.format(sql_str, openid)
    print(sql_str)
    res, pk = db_utils.execute_insert_sql_and_get_primary_key(sql_str)
    return res,pk


def update_goods_data_by_id(openid, goods_id,kwargs):
    column_name_list = get_table_column_name("goods_info")
    sql_str = 'update goods_info set '
    for k, v in kwargs.items():
        if k in can_not_update_string_list:
            continue
        if k in column_name_list:
            if k in need_escapr_string_list:  # 如果该字段需要转义
                if v != None:
                    v = db_utils.escape_string(v)
            sql_str += '{0}="{1}",'.format(k, v)
    sql_str = '{0} where openid = "{1}" and id = "{2}" '.format(sql_str[:-1], openid,goods_id)
    print(sql_str)
    res, _ = db_utils.execute_single_sql(sql_str)
    return res

def get_goods_data(openid,goods_id):
    sql = """
    select * from goods_info where openid = "{openid}"  "{goods_filter}"
    """.format(openid=openid,goods_filter=" and id = {0}".format(goods_id) if goods_id else "")
    return db_utils.execute_single_sql(sql)

def get_store_goods_data(openid,store_id):
    sql = """
    select * from goods_info where openid = "{openid}"  and store_id = "{store_id}"
    """.format(openid=openid,store_id=store_id)
    return db_utils.execute_single_sql(sql)