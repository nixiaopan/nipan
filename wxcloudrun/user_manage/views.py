import traceback
import json
from wxcloudrun.utils.logger import logger
from wxcloudrun.commons.constant import ResponsCode, IdentityType
from wxcloudrun.mapper.user_info import insert_user_data, update_user_data, get_user_data
from wxcloudrun.utils.decorators import get_params, json_response
from wxcloudrun.utils.exception import InvalidParameter


def user_param_check(phone_number=None, identity_type=None):
    if phone_number and len(phone_number) != 11:
        raise InvalidParameter('手机号长度异常')
    if identity_type and int(identity_type) not in [IdentityType.ANCHOR, IdentityType.BUSINESSES]:
        raise InvalidParameter('用户类型异常')


@json_response
@get_params
def user_register(request, openid, identity_type, icon, pet_name):
    """
    用户注册，只能注册一次
    :request method: POST
    :param identity_type: 1是主播，2是商户
    :param icon: 用户头像路径
    :param pet_name: 用户昵称
    :return:code：200成功，450失败，550异常
    {'code': ResponsCode.FAILED, 'data': '', "msg": '注册失败'}
    {'code': ResponsCode.SUCCESS, 'data': '', "msg": '注册成功'}
    {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '注册异常'}
    """
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '注册失败'}
    try:
        user_param_check(identity_type=identity_type)
        is_success = insert_user_data(openid, identity_type, icon, pet_name)
        if is_success:
            rsp = {'code': ResponsCode.SUCCESS, 'data': '', "msg": '注册成功'}
    except InvalidParameter as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '注册异常'}
    finally:
        return rsp


@json_response
@get_params
def update_user_info(request, openid):
    """
    修改用户信息，以下参数传啥改啥
    :request method: POST
    :param phone_number: 手机号
    :param shipping_address:收货地址
    :param wechat:微信号
    :param job_title: 职位（第一个版本应该不要）
    :param real_name:真实姓名（或者说收货人姓名）
    :return: code：200成功，450失败，550异常
    {'code': ResponsCode.FAILED, 'data': '', "msg": '修改失败'}，
    {'code': ResponsCode.SUCCESS, 'data': '', "msg": '修改成功'}
    {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '修改异常'}
    """
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '修改失败'}
    try:
        is_success = update_user_data(openid, json.loads(request.body))
        if is_success:
            rsp = {'code': ResponsCode.SUCCESS, 'data': '', "msg": '修改成功'}
    except InvalidParameter as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        # logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '修改异常'}
    finally:
        return rsp


@json_response
@get_params
def get_user_info(request, openid):
    '''
    获取当前用户的信息
    :request method: GET
    :return:code：200成功，450失败，550异常
    {'code': ResponsCode.FAILED, 'data': '', "msg": '获取失败'}
    {'code': ResponsCode.SUCCESS, 'data': user_data, "msg": '获取成功'}
    {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '获取异常'}
    '''
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '获取失败'}
    try:
        is_success, user_data = get_user_data(openid)
        if user_data:
            rsp = {'code': ResponsCode.SUCCESS, 'data': user_data[0], "msg": '获取成功'}
        else:
            rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '没有该用户'}
    except InvalidParameter as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '获取异常'}
    finally:
        return rsp
