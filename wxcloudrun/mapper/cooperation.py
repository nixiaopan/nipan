# -*- coding: utf-8 -*-
'''
@author: nixiaopan
@time: 2022/4/9 23:58
'''
from wxcloudrun.mapper.utils import get_table_column_name
from wxcloudrun.utils.SQL.DBUtils import db_utils

need_escape_string_list=["goods_url", "pic_path", "brand", "goods_name", "specification",
                        "selling_point","storage_condition","unsuitable_people", "daily_price","lowest_price",
                         "tmall_price","taobao_price","other_price","live_price", "preferential_way","delivery_company",
                         "shipping_addresses","free_shipping","not_shipping","comment","test_comment","store_name"]
can_not_update_string_list = ["openid","id","merchant_openid","status"]

def insert_cooperation_data(merchant_openid,kwargs):
    column_name_list = get_table_column_name("cooperation")
    sql_str = 'insert into  cooperation set '
    for k, v in kwargs.items():
        if k in column_name_list:
            if k in need_escape_string_list:  # 如果该字段需要转义
                if v != None:
                    v = db_utils.escape_string(v)
            sql_str += '{0}="{1}",'.format(k, v)
    sql_str = '{0} merchant_openid = "{1}"'.format(sql_str, merchant_openid)
    print(sql_str)
    res, _ = db_utils.execute_single_sql(sql_str)
    return res



def get_cooperation_status_for_update(cooperation_id,cur_db_util=None):
    sql = """
    select status from cooperation where id = "{cooperation_id}" for update
    """.format(cooperation_id=cooperation_id)
    if cur_db_util:
        data = cur_db_util.execute_single_sql_in_transaction(sql)
    else:
        res, data = db_utils.execute_single_sql(sql)
    return data

def update_cooperation_data(cooperation_id,cur_db_util,kwargs):
    column_name_list = get_table_column_name("cooperation")
    sql_str = 'update  cooperation set '
    for k, v in kwargs.items():
        if k in can_not_update_string_list:
            continue
        if k in column_name_list:
            if k in need_escape_string_list:  # 如果该字段需要转义
                if v != None:
                    v = db_utils.escape_string(v)
            sql_str += '{0}="{1}",'.format(k, v)
    sql_str = '{0} where id = "{1}"'.format(sql_str[:-1], cooperation_id)
    print(sql_str)
    cur_db_util.execute_single_sql_in_transaction(sql_str)

def update_cooperation_status(cooperation_id,anchor_openid,new_status,old_status,cur_db_util=None):
    sql = """
    update cooperation set anchor_openid = "{anchor_openid}", status ={new_status} where id = "{cooperation_id}" and status = {old_status}
    """.format(cooperation_id=cooperation_id,anchor_openid=anchor_openid,new_status =new_status,old_status=old_status)
    if cur_db_util:
        res = cur_db_util.execute_single_sql_in_transaction(sql)
    else:
        res, _ = db_utils.execute_single_sql(sql)
    return res

def update_cooperation_status_and_set_shipping_info(cooperation_id,new_status,old_status,anchor_shipping_address,
                                                    anchor_phone_number,anchor_name,sample_count,cur_db_util=None):
    sql = """
    update cooperation set status ={new_status}, anchor_shipping_address="{anchor_shipping_address}", 
    anchor_phone_number="{anchor_phone_number}",anchor_name="{anchor_name}",sample_count="{sample_count}" where id = "{cooperation_id}" and status = {old_status}
    """.format(cooperation_id=cooperation_id,new_status =new_status,old_status=old_status,anchor_shipping_address=db_utils.escape_string(anchor_shipping_address),
               anchor_name=db_utils.escape_string(anchor_name),anchor_phone_number=db_utils.escape_string(anchor_phone_number),sample_count=sample_count)
    if cur_db_util:
        res = cur_db_util.execute_single_sql_in_transaction(sql)
    else:
        res, _ = db_utils.execute_single_sql(sql)
    return res

def update_cooperation_status_and_set_sample_courier_number(cooperation_id,new_status,old_status,sample_courier_number,cur_db_util=None):
    sql = """
    update cooperation set status ={new_status}, sample_courier_number="{sample_courier_number}" where id = "{cooperation_id}" and status = {old_status}
    """.format(cooperation_id=cooperation_id,new_status =new_status,old_status=old_status,sample_courier_number=db_utils.escape_string(sample_courier_number))
    if cur_db_util:
        res = cur_db_util.execute_single_sql_in_transaction(sql)
    else:
        res, _ = db_utils.execute_single_sql(sql)
    return res


def update_cooperation_status_and_set_test_result(cooperation_id,new_status,old_status,test_result,test_comment,cur_db_util=None):
    sql = """
    update cooperation set status ={new_status}, test_result="{test_result}",test_comment="{test_comment}" where id = "{cooperation_id}" and status = {old_status}
    """.format(cooperation_id=cooperation_id,new_status =new_status,old_status=old_status,test_result=test_result,
               test_comment=db_utils.escape_string(test_comment) if test_comment else "")
    if cur_db_util:
        res = cur_db_util.execute_single_sql_in_transaction(sql)
    else:
        res, _ = db_utils.execute_single_sql(sql)
    return res


def get_cooperation_data_for_update(cooperation_id,cur_db_util=None):
    sql = """
    select * from cooperation where id = "{cooperation_id}" for update
    """.format(cooperation_id=cooperation_id)
    if cur_db_util:
        data = cur_db_util.execute_single_sql_in_transaction(sql)
    else:
        res, data = db_utils.execute_single_sql(sql)
    return data


def get_cooperation_data_by_status(status,openid,openid_name,test_result,start,count):
    sql = """
    select * from cooperation  where status = "{status}" and {openid_name} = "{openid}" {test_result_filter} order by create_time 
    limit {start}, {count}
    """.format(status=status,openid=openid,openid_name=openid_name,test_result_filter="and test_result = '{0}'".format(test_result) if test_result else "",
               start=start,count=count)
    print(sql)
    res, data = db_utils.execute_single_sql(sql)
    return data