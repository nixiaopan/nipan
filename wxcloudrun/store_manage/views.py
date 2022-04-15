import traceback
import json
from wxcloudrun.utils.logger import logger
from wxcloudrun.commons.constant import ResponsCode
from wxcloudrun.mapper.store_info import insert_store_info,update_store_data,get_store_data,delet_store_data
from wxcloudrun.utils.decorators import get_params,json_response


@json_response
@get_params
def new_store(request,openid,store_id,store_name,drs):
    """
    :request method: POST
    :param openid: 用户唯一标识（无需上传）
    :param store_id: 店铺长id(最长45位)
    :param store_name: 店铺名(最长45位)
    :param drs: 店铺DRS评分
    :return:code：200成功，450失败，550异常
            {'code': ResponsCode.FAILED, 'data': '', "msg": '添加商店失败'}
            {'code': ResponsCode.SUCCESS, 'data': '',"msg":'添加商店成功'}
            {'code': ResponsCode.EXCEPTION, 'data': '',"msg":'添加商店异常'}

    """
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '添加商店失败'}
    try:
        is_success = insert_store_info(store_id,store_name,drs,openid)
        if is_success:
            rsp = {'code': ResponsCode.SUCCESS, 'data': '',"msg":'添加商店成功'}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '',"msg":'添加商店异常'}
    finally:
        return rsp

@json_response
@get_params
def update_store_info(request,openid,store_id):
    """
    :request method: POST
    :param openid: 用户唯一标识（无需上传）
    :param store_id: 店铺长id(最长45位)(必传)
    :param store_name: 店铺名（非必填）(最长45位)
    :param drs: 店铺DRS评分（非必填）
    :return:code：200成功，450失败，550异常
    {'code': ResponsCode.FAILED, 'data': '', "msg": '修改失败'}，
    {'code': ResponsCode.SUCCESS, 'data': '', "msg": '修改成功'}
    {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '修改异常'}
    """
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '修改失败'}
    try:
        print(request.body)
        is_success = update_store_data(openid,store_id,json.loads(request.body))
        if is_success:
            rsp = {'code': ResponsCode.SUCCESS, 'data': '', "msg": '修改成功'}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '修改异常'}
    finally:
        return rsp

@json_response
@get_params
def delete_store(request,openid,store_id):
    """
    :request method: POST
    :param openid: 用户唯一标识（无需上传）
    :param store_id: 店铺长id(最长45位)(必传)
    :return:code：200成功，450失败，550异常
    {'code': ResponsCode.FAILED, 'data': '', "msg": '删除失败'}，
    {'code': ResponsCode.SUCCESS, 'data': '', "msg": '删除成功'}
    {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '删除异常'}
    """
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '删除失败'}
    try:
        print(request.body)
        is_success = delet_store_data(openid,store_id)
        if is_success:
            rsp = {'code': ResponsCode.SUCCESS, 'data': '', "msg": '删除成功'}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '删除异常'}
    finally:
        return rsp

@json_response
@get_params
def get_store_info(request,openid):
    """
    :request method: GET
    :param openid: 用户唯一标识（无需上传）
    :return:code：200成功，450失败，550异常
    {'code': ResponsCode.FAILED, 'data': '', "msg": '获取失败'}，
    {'code': ResponsCode.SUCCESS, 'data': store_info, "msg": '获取成功'}
    {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '获取异常'}
    """
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '获取失败'}
    try:
        is_success,store_info = get_store_data(openid)
        if is_success:
            rsp = {'code': ResponsCode.SUCCESS, 'data': store_info, "msg": '获取成功'}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '获取异常'}
    finally:
        return rsp

