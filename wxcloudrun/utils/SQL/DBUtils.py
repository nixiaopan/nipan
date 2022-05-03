# -*- coding: utf-8 -*-
'''
@Time   : 2018-12-10 16:59
@Author : yuyichen
'''
import traceback
from django.db import connection
from contextlib import contextmanager
from pymysql.converters import escape_string
from wxcloudrun.utils.logger import logger

TIMEOUT_THREAD = 10  # 连接超时时间


class DBUtils:
    def __init__(self):
        # 初始化数据库配置
        self.conn = None  # 为执行事务使用
        self.cursor = None  # 为执行事务使用

    def _connection_init(self):
        '''
        连接初始化
        :return: 返回conn, cursor。如果连接失败返回None, None
        '''
        conn = cursor = None
        try:
            conn = connection
            cursor = conn.cursor()
            return conn, cursor
        except Exception as e:
            print('except in _connection_init {0}'.format(e))
            self._connection_release(conn, cursor)
            return None, None

    def _connection_release(self, conn, cursor):
        '''
        关闭数据库相关连接
        :param conn:
        :param cursor:
        :return:
        '''
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass

    def dictfetchall(self, cursor):
        "Return all rows from a cursor as a dict"

        data = cursor.fetchall()
        if data:
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in data]
        else:
            return None

    def execute_single_sql(self, sql_str):
        '''
        执行单条sql语句
        :param sql_str:
        :return: 执行成功会返回True和执行的结果数据，执行失败会返回False, None
        '''
        conn, cursor = self._connection_init()
        if not conn or not cursor:
            return False, None
        try:
            cursor.execute(sql_str)
            data = self.dictfetchall(cursor)
            conn.commit()
            return True, data
        except Exception as e:
            traceback.print_exc()
            logger.exception('except in execute_single_sql {0} {1}'.format(e, sql_str))
            if 'timeout exceeded' in str(e):
                return 'time exceed', None
            else:
                return False, None
        finally:
            self._connection_release(conn, cursor)

    def execute_insert_sql_and_get_primary_key(self, sql_str):
        '''
        执行单条sql语句，并返回插入的主键
        :param sql_str:
        :return: 执行成功会返回True和主键，执行失败会返回False, 0
        '''
        conn, cursor = self._connection_init()
        if not conn or not cursor:
            return False, None
        try:
            cursor.execute(sql_str)
            last_pk = int(cursor.lastrowid)
            cursor.fetchall()
            conn.commit()
            return True, last_pk
        except Exception as e:
            logger.exception('except in execute_insert_sql_and_get_primary_key {0} {1}'.format(e, sql_str))
            return False, 0
        finally:
            self._connection_release(conn, cursor)

    def execute_sql_list(self, sql_str_list):
        '''
        执行多条sql语句，并返回最终结果。如果失败会回滚。
        :param sql_str_list:
        :return: 执行成功会返回True和执行的结果数据，执行失败会返回False, None，并回滚
        '''
        if not isinstance(sql_str_list, list):
            return False, None
        conn, cursor = self._connection_init()
        if not conn or not cursor:
            return False, None
        exception_sql_str = None
        try:
            for sql_str in sql_str_list:
                exception_sql_str = sql_str
                cursor.execute(sql_str)
            data = cursor.fetchall()
            conn.commit()
            return True, data
        except Exception as e:
            logger.exception('except in execute_sql_list {0} {1}'.format(e, exception_sql_str))
            conn.rollback()
            return False, None
        finally:
            self._connection_release(conn, cursor)

    def execute_many_sql(self, sql_str_template, items):
        '''
        批量执行
        :param sql_str_template: 模板sql语句
        :param items: 元组形式的数据，用于insert或者update
        :return:
        '''
        conn, cursor = self._connection_init()
        if not conn or not cursor:
            return False, None
        try:
            cursor.executemany(sql_str_template, items)
            conn.commit()
            return True
        except Exception as e:
            logger.exception('except in execute_many_sql {0} {1}'.format(e, sql_str_template))
            return False
        finally:
            self._connection_release(conn, cursor)

    def escape_string(self, raw):
        try:
            escaped_str = escape_string(raw)
        except:
            traceback.print_exc()
            escaped_str = ''
        return escaped_str

    '''
    事务相关的异常不处理，直接抛出。在具体调用的地方进行捕获。
    '''

    def begin_transaction(self):
        # 开启事务，获取对象的连接
        self.conn, self.cursor = self._connection_init()

    def execute_single_sql_in_transaction(self, sql_str):
        # 在事务中执行单条sql语句
        self.cursor.execute(sql_str)
        data = self.dictfetchall(self.cursor)
        return data

    def execute_insert_sql_and_get_primary_key_in_transaction(self, sql_str):
        # 在事务中执行单条insert sql语句，并获取新插入的主键
        self.cursor.execute(sql_str)
        last_pk = int(self.cursor.lastrowid)
        return last_pk

    def execute_many_sql_in_transaction(self, sql_str_template, items):
        # 在事务中批量执行sql语句
        self.cursor.executemany(sql_str_template, items)

    def commit_in_transaction(self):
        # 在事务中提交
        self.conn.commit()

    def deal_with_transation_exception(self):
        # 事务执行中出现异常之后的处理，回滚。在except中使用。
        if self.conn:
            self.conn.rollback()

    def end_transaction(self):
        # 在finally中使用。
        # 先解锁表
        try:
            self.cursor.execute('unlock tables')
        except Exception as e:
            pass
        # 关闭事务
        self._connection_release(self.conn, self.cursor)

    @contextmanager
    def transcontext(self, need_raise_exception=False):
        try:
            self.begin_transaction()
            yield
        except Exception as e:
            self.deal_with_transation_exception()
            if need_raise_exception:
                raise e
        else:
            self.commit_in_transaction()
        finally:
            self.end_transaction()


db_utils = DBUtils()
