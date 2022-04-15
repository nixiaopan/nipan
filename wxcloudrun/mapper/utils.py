# -*- coding: utf-8 -*-
'''
@author: nixiaopan
@time: 2022/4/9 13:25
'''
from wxcloudrun.utils.SQL.DBUtils import db_utils
def get_table_column_name(table):
    '''
    获取表中的所有的字段
    :return:
    '''
    column_name_list = []
    sql = '''
            select  column_name as column_name from information_schema.columns where table_schema ='django_demo'  and table_name = "{table}"
            '''.format(table=table)
    print(sql)
    _, results = db_utils.execute_single_sql(sql)
    if results:
        for result in results:
            column_name_list.append(result.get('column_name'))
    return column_name_list