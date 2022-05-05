# -*- coding: utf-8 -*-
'''
@author: nixiaopan
@time: 2022/3/30 21:36
'''
from wxcloudrun.mapper.utils import get_table_column_name
from wxcloudrun.utils.SQL.DBUtils import db_utils

need_escapr_string_list = ["shipping_address", "job_title", "wechat", "pet_name"]
can_not_update_string_list = ["openid", "identity_type"]


def insert_user_data(openid, identity_type, icon, pet_name):
    sql_str = '''
    insert into  user_info set openid = "{openid}", identity_type="{identity_type}",icon="{icon}",pet_name = "{pet_name}"
    '''.format(openid=openid, identity_type=identity_type, icon=icon, pet_name=db_utils.escape_string(pet_name))
    print(sql_str)
    is_success, data = db_utils.execute_single_sql(sql_str)
    return is_success


def update_user_data(openid, kwargs):
    column_name_list = get_table_column_name("user_info")
    sql_str = 'update user_info set '
    for k, v in kwargs.items():
        if k in can_not_update_string_list:
            continue
        if k in column_name_list:
            if k in need_escapr_string_list:  # 如果该字段需要转义
                if v != None:
                    v = db_utils.escape_string(v)
            sql_str += '{0}="{1}",'.format(k, v)
    sql_str = '{0} where openid = "{1}"'.format(sql_str[:-1], openid)
    print(sql_str)
    res, _ = db_utils.execute_single_sql(sql_str)
    return res


def get_user_data(openid):
    sql_str = '''
            select * from user_info where openid = '{openid}'
            '''.format(openid=openid)
    print(sql_str)
    is_success, data = db_utils.execute_single_sql(sql_str)
    return is_success, data

def get_user_data_dict():
    sql_str = '''
            select * from user_info
            '''
    print(sql_str)
    user_data_dict = {}
    is_success, data = db_utils.execute_single_sql(sql_str)

    for row in data:
        user_data_dict[row.get("openid")] = row
    return user_data_dict