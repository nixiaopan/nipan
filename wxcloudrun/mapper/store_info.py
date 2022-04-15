# -*- coding: utf-8 -*-
'''
@author: nixiaopan
@time: 2022/3/30 21:36
'''
from wxcloudrun.mapper.utils import get_table_column_name
from wxcloudrun.utils.SQL.DBUtils import db_utils

need_escapr_string_list = ["store_name"]
can_not_update_string_list = ["openid","store_id"]



def insert_store_info(store_id,store_name,drs,openid):
    sql_str = '''
    insert into  store_info set store_id = "{store_id}", store_name="{store_name}",drs="{drs}",openid="{openid}"
    '''.format(store_id=store_id, store_name=db_utils.escape_string(store_name), drs=drs,openid=openid)
    print(sql_str)
    is_success, data = db_utils.execute_single_sql(sql_str)
    return is_success

def update_store_data(openid, store_id,kwargs):
    column_name_list = get_table_column_name("store_info")
    sql_str = 'update store_info set '
    for k, v in kwargs.items():
        if k in can_not_update_string_list:
            continue
        if k in column_name_list:
            if k in need_escapr_string_list:  # 如果该字段需要转义
                if v != None:
                    v = db_utils.escape_string(v)
            sql_str += '{0}="{1}",'.format(k, v)
    sql_str = '{0} where openid = "{1}" and store_id = "{2}"'.format(sql_str[:-1], openid,store_id)
    print(sql_str)
    res, _ = db_utils.execute_single_sql(sql_str)
    return res

def get_store_data(openid):
    sql_str = '''
            select store_id, store_name, drs from store_info where openid = '{openid}'
            '''.format(openid=openid)
    print(sql_str)
    is_success, data = db_utils.execute_single_sql(sql_str)
    return is_success,data

def get_store_data_by_store_id(openid,store_id):
    sql_str = '''
            select store_id, store_name, drs from store_info where openid = '{openid}' and store_id ="{store_id}"
            '''.format(openid=openid,store_id=store_id)
    print(sql_str)
    is_success, data = db_utils.execute_single_sql(sql_str)
    return is_success,data

def delet_store_data(openid,store_id):
    sql_str = '''
            delete from store_info where openid = '{openid}' and store_id = "{store_id}"
            '''.format(openid=openid,store_id=store_id)
    print(sql_str)
    is_success, data = db_utils.execute_single_sql(sql_str)
    return is_success,data