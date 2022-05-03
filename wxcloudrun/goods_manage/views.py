import traceback
import json
from wxcloudrun.utils.exception import InvalidParameter
from wxcloudrun.utils.logger import logger
from wxcloudrun.commons.constant import ResponsCode
from wxcloudrun.mapper.goods_info import insert_goods_data, update_goods_data_by_id, get_goods_data, \
    get_store_goods_data
from wxcloudrun.mapper.store_info import get_store_data_by_store_id
from wxcloudrun.utils.decorators import get_params, json_response
from wxcloudrun.mapper.store_info import insert_store_info


@json_response
@get_params
def add_goods(request, openid, store_id,
              specification, brand, favorable_rate, pic_path, live_recording_screen_path, daily_price, commission_rate,
              pos_price, preferential_way, goods_url, hand_card,
              storage_condition, shelf_life, unsuitable_people, ability_to_deliver, shipping_cycle, shipping_addresses,
              delivery_company, not_shipping):
    """
    :request method: POST
    商铺信息
    :param store_id: 店铺id(最长45位)
    商品信息
    :param goods_name: 商品名称
    :param specification: 规格
    :param brand: 商品品牌
    :param favorable_rate: 好评率
    :param pic_path: 商品主图链接（列表）
    :param live_recording_screen_path: 知名主播带货视频链接
    :param daily_price: 日常价格
    :param live_price: 直播价格
    :param commission_rate: 直播佣金比例
    :param pos_price: 坑位费预算
    :param preferential_way: 直播活动机制
    :param goods_url: 商品链接
    :param hand_card: 直播手卡
    全网比价
    :param tmall_price: 天猫价格
    :param taobao_price: 淘宝价格
    :param jd_price: 京东
    :param pdd_price: 拼多多
    :param offline_price: 线下商超
    存储与运输
    :param storage_condition: 存储条件
    :param shelf_life: 保质期
    :param unsuitable_people: 不适用人群
    :param ability_to_deliver: 发货能力
    :param shipping_cycle: 发货周期
    :param shipping_addresses: 发货地址
    :param delivery_company: 物流快递公司
    :param not_shipping: 不发货区域
    :param free_shipping: 包邮地区
    其他
    :param comment: 备注信息
    :return:
    {'code': ResponsCode.FAILED, 'data': '', "msg": '添加商品失败'}
    {'code': ResponsCode.SUCCESS, 'data': {"goods_id": pk}, "msg": '添加商品成功'}
    {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '添加商品异常'}
    """
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '添加商品失败'}

    try:
        _, data = get_store_data_by_store_id(openid, store_id)
        if not data:
            raise InvalidParameter('店铺不存在')
        is_success, pk = insert_goods_data(openid, json.loads(request.body))
        if is_success:
            rsp = {'code': ResponsCode.SUCCESS, 'data': {"goods_id": pk}, "msg": '添加商品成功'}
    except InvalidParameter as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '添加商品异常'}
    finally:
        return rsp


@json_response
@get_params
def update_goods(request, openid, goods_id, store_id):
    """
    修改商品信息，传啥改啥，goods_id，store_id必传
    :request method: POST
    商铺信息
    :param store_id: 店铺id(最长45位)
    商品信息
    :param goods_id:商品id
    :param goods_name: 商品名称
    :param specification: 规格
    :param brand: 商品品牌
    :param favorable_rate: 好评率
    :param pic_path: 商品主图链接（列表）
    :param live_recording_screen_path: 知名主播带货视频链接
    :param daily_price: 日常价格
    :param live_price: 直播价格
    :param commission_rate: 直播佣金比例
    :param pos_price: 坑位费预算
    :param preferential_way: 直播活动机制
    :param goods_url: 商品链接
    :param hand_card: 直播手卡
    全网比价
    :param tmall_price: 天猫价格
    :param taobao_price: 淘宝价格
    :param jd_price: 京东
    :param pdd_price: 拼多多
    :param offline_price: 线下商超
    存储与运输
    :param storage_condition: 存储条件
    :param shelf_life: 保质期
    :param unsuitable_people: 不适用人群
    :param ability_to_deliver: 发货能力
    :param shipping_cycle: 发货周期
    :param shipping_addresses: 发货地址
    :param delivery_company: 物流快递公司
    :param not_shipping: 不发货区域
    :param free_shipping: 包邮地区
    其他
    :param comment: 备注信息
    :return:
    {'code': ResponsCode.FAILED, 'data': '', "msg": '更新商品失败'}
    {'code': ResponsCode.SUCCESS, 'data': '', "msg": '更新商品成功'}
    {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '更新商品异常'}
    """
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '更新商品失败'}

    try:
        _, data = get_store_data_by_store_id(openid, store_id)
        if not data:
            raise InvalidParameter('店铺不存在')
        is_success = update_goods_data_by_id(openid, goods_id, json.loads(request.body))
        if is_success:
            rsp = {'code': ResponsCode.SUCCESS, 'data': '', "msg": '更新商品成功'}
    except InvalidParameter as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '更新商品异常'}
    finally:
        return rsp


@json_response
@get_params
def get_goods_info(request, openid, goods_id=None):
    """
    获取商铺信息
    :request method: POST
    :param goods_id: 商品id,不传返回该用户所有的商品，传了返回该商品信息
    :return:
    {'code': ResponsCode.SUCCESS, 'data': all_goods, "msg": '获取商品成功'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '获取商品失败'}
    {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '获取商品异常'}
    """
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '获取商品失败'}
    try:
        is_success, all_goods = get_goods_data(openid, goods_id)
        if is_success:
            rsp = {'code': ResponsCode.SUCCESS, 'data': all_goods, "msg": '获取商品成功'}
    except InvalidParameter as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '获取商品异常'}
    finally:
        return rsp


@json_response
@get_params
def get_store_goods_info(request, openid, store_id):
    """
    获取某商铺下的所有商品信息
    :request method: POST
    :store_id: 商铺ID
    :return:
    {'code': ResponsCode.FAILED, 'data': '', "msg": '获取商品失败'}
    {'code': ResponsCode.SUCCESS, 'data': all_goods, "msg": '获取商品成功'}
    {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '获取商品异常'}
    """
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '获取商品失败'}
    try:
        is_success, all_goods = get_store_goods_data(openid, store_id)
        if is_success:
            rsp = {'code': ResponsCode.SUCCESS, 'data': all_goods, "msg": '获取商品成功'}
    except InvalidParameter as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '获取商品异常'}
    finally:
        return rsp
