import json
import logging

from django.http import JsonResponse

logger = logging.getLogger('log')
from wxcloudrun.utils.SQL.DBUtils import DBUtils


def test1(request):
    """
    获取当前计数

     `` request `` 请求对象
    """
    # 使用 cursor() 方法创建一个游标对象 cursor
    # print(Test.objects.all())
    print(request.headers)
    logger.info(request.headers)
    str = request.POST.get("a")
    db_utils = DBUtils()
    _, data = db_utils.execute_single_sql('''insert into  test set msg = "%s" ''' % (db_utils.escape_string(str)))
    rsp = JsonResponse({'code': 0, 'errorMsg': '力哥真帅'}, json_dumps_params={'ensure_ascii': False})
    # Test.objects.create(msg="where id = 1")

    return rsp
