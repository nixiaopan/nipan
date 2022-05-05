# -*- coding: utf-8 -*-
'''
@author: nixiaopan
@time: 2022/4/9 23:58
'''
import logging

from wxcloudrun.mapper.utils import get_table_column_name
from wxcloudrun.utils.SQL.DBUtils import db_utils

need_escape_string_list = ["goods_name", "specification", "brand", "favorable_rate", "pic_path",
                           "live_recording_screen_path", "daily_price", "live_price",
                           "preferential_way", "goods_url", "hand_card", "tmall_price", "taobao_price", "jd_price",
                           "pdd_price", "offline_price", "storage_condition", "shelf_life", "unsuitable_people",
                           "shipping_cycle", "shipping_addresses", "delivery_company", "not_shipping",
                           "free_shipping", "comment", "test_comment", "store_name"]
can_not_update_string_list = ["openid", "id", "merchant_openid", "status"]


def insert_cooperation_data(merchant_openid, kwargs):
    column_name_list = get_table_column_name("cooperation")
    sql_str = 'insert into  cooperation set '
    for k, v in kwargs.items():
        if k in column_name_list:
            if k in need_escape_string_list:  # 如果该字段需要转义
                if k == "pic_path":
                    v = ",".join(v)
                if v != None:
                    v = db_utils.escape_string(v)
            sql_str += '{0}="{1}",'.format(k, v)
    sql_str = '{0} merchant_openid = "{1}"'.format(sql_str, merchant_openid)
    print(sql_str)
    res, pk = db_utils.execute_insert_sql_and_get_primary_key(sql_str)
    return res, pk


def get_cooperation_status_for_update(cooperation_id, cur_db_util=None):
    sql = """
    select status from cooperation where id = "{cooperation_id}" for update
    """.format(cooperation_id=cooperation_id)
    if cur_db_util:
        data = cur_db_util.execute_single_sql_in_transaction(sql)
    else:
        res, data = db_utils.execute_single_sql(sql)
    return data


def update_cooperation_data(cooperation_id, cur_db_util, kwargs):
    column_name_list = get_table_column_name("cooperation",cur_db_util)
    sql_str = 'update  cooperation set '
    for k, v in kwargs.items():
        if k in can_not_update_string_list:
            continue
        if k in column_name_list:
            if k in need_escape_string_list:  # 如果该字段需要转义
                if k == "pic_path":
                    v = ",".join(v)
                if v is not None:
                    v = cur_db_util.escape_string(v)
            sql_str += '{0}="{1}",'.format(k, v)
    sql_str = '{0} where id = "{1}"'.format(sql_str[:-1], cooperation_id)
    print(sql_str)

    cur_db_util.execute_single_sql_in_transaction(sql_str)


def update_cooperation_status(cooperation_id, anchor_openid, new_status, old_status, cur_db_util=None):
    sql = """
    update cooperation set anchor_openid = "{anchor_openid}", status ={new_status} where id = "{cooperation_id}" and status = {old_status}
    """.format(cooperation_id=cooperation_id, anchor_openid=anchor_openid, new_status=new_status, old_status=old_status)
    if cur_db_util:
        res = cur_db_util.execute_single_sql_in_transaction(sql)
    else:
        res, _ = db_utils.execute_single_sql(sql)
    return res


def update_cooperation_status_and_set_shipping_info(cooperation_id, new_status, old_status, anchor_shipping_address,
                                                    anchor_phone_number, anchor_name, sample_count, sample_comment, cur_db_util=None):
    sql = """
    update cooperation set status ={new_status}, anchor_shipping_address="{anchor_shipping_address}", 
    anchor_phone_number="{anchor_phone_number}",anchor_name="{anchor_name}",sample_count="{sample_count}",
    sample_comment = "{sample_comment}" where id = "{cooperation_id}" and status = {old_status}
    """.format(cooperation_id=cooperation_id, new_status=new_status, old_status=old_status,
               anchor_shipping_address=db_utils.escape_string(anchor_shipping_address),
               anchor_name=db_utils.escape_string(anchor_name),
               anchor_phone_number=db_utils.escape_string(anchor_phone_number), sample_count=sample_count,
               sample_comment=db_utils.escape_string(sample_comment))
    if cur_db_util:
        res = cur_db_util.execute_single_sql_in_transaction(sql)
    else:
        res, _ = db_utils.execute_single_sql(sql)
    return res


def update_cooperation_status_and_set_sample_courier_number(cooperation_id, new_status, old_status,
                                                            sample_courier_number, cur_db_util=None):
    sql = """
    update cooperation set status ={new_status}, sample_courier_number="{sample_courier_number}" where id = "{cooperation_id}" and status = {old_status}
    """.format(cooperation_id=cooperation_id, new_status=new_status, old_status=old_status,
               sample_courier_number=db_utils.escape_string(sample_courier_number))
    if cur_db_util:
        res = cur_db_util.execute_single_sql_in_transaction(sql)
    else:
        res, _ = db_utils.execute_single_sql(sql)
    return res


def update_cooperation_status_and_set_test_result(cooperation_id, new_status, old_status, test_result, test_failed_reason, test_comment,
                                                  cur_db_util=None):
    sql = """
    update cooperation set status ={new_status}, test_result="{test_result}",test_failed_reason="{test_failed_reason}",test_comment="{test_comment}"  where id = "{cooperation_id}" and status = {old_status}
    """.format(cooperation_id=cooperation_id, new_status=new_status, old_status=old_status, test_result=test_result,
               test_failed_reason=db_utils.escape_string(test_failed_reason),
               test_comment=db_utils.escape_string(test_comment) if test_comment else "")
    if cur_db_util:
        res = cur_db_util.execute_single_sql_in_transaction(sql)
    else:
        res, _ = db_utils.execute_single_sql(sql)
    return res


def get_cooperation_data_for_update(cooperation_id, cur_db_util=None):
    sql = """
    select * from cooperation where id = "{cooperation_id}" for update
    """.format(cooperation_id=cooperation_id)
    if cur_db_util:
        data = cur_db_util.execute_single_sql_in_transaction(sql)
    else:
        res, data = db_utils.execute_single_sql(sql)
    return data


def get_cooperation_data_by_status(status, openid, openid_name, test_result, start, count):
    sql = """
    select * from cooperation  where status = "{status}" and {openid_name} = "{openid}" {test_result_filter} order by create_time 
    limit {start}, {count}
    """.format(status=status, openid=openid, openid_name=openid_name,
               test_result_filter="and test_result = '{0}'".format(test_result) if test_result else "",
               start=start, count=count)
    print(sql)
    res, data = db_utils.execute_single_sql(sql)
    return data
