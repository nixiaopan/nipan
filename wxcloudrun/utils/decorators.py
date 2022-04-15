
import functools
import inspect
import json
from wxcloudrun.utils.logger import logger
from wxcloudrun.commons.constant import ResponsCode
from wxcloudrun.config import IS_TEST_ENV
from django.http import JsonResponse

def get_params(func):
    func_params = inspect.signature(func).parameters

    def pick_params(params, json_params):
        param_dict = dict()
        for key in params:
            if key == "request" or key == "openid":
                continue
            default_value = params.get(key).default
            if key not in json_params and default_value == inspect.Parameter.empty:
                return False, "请求中缺少参数: {}".format(key)
            if json_params.get(key):
                param_dict[key] = str(json_params.get(key, default_value))
        return True, param_dict

    def get_openid(request):
        if IS_TEST_ENV:
            return "oJ92T5V3wWVuP55sPZytRYjGulf8"
        try:
            openid = request.headers.get("X-Wx-Openid")
            return openid
        except:
            return None

    @functools.wraps(func)
    def wrapper(request):
        openid = get_openid(request)
        if not openid:
            return {"code": ResponsCode.FAILED, "msg": "无法获取openid信息", "data": ""}
        if request.method == "POST":
            try:
                json_params = json.loads(request.body)
                logger.info(json_params)
            except:
                return {"code": ResponsCode.FAILED, "msg": "参数必须为json形式", "data": ""}
            success, data = pick_params(func_params, json_params)
            if success:
                return func(request,openid,**data)
            else:
                return {"code": ResponsCode.FAILED, "msg": data, "data":""}
        elif request.method == "GET":
            return func(request, openid)
        else:
            return {"code": ResponsCode.FAILED, "msg": "未知的method", "data": ""}

    return wrapper


def json_response(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        logger.info(data)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
    return wrapper
