import traceback
import json
from wxcloudrun.utils.exception import InvalidParameter
from wxcloudrun.utils.logger import logger
from wxcloudrun.commons.constant import ResponsCode
from wxcloudrun.mapper.goods_info import insert_goods_data,update_goods_data_by_id,get_goods_data,get_store_goods_data
from wxcloudrun.mapper.store_info import get_store_data_by_store_id
from wxcloudrun.utils.decorators import get_params,json_response


@json_response
@get_params
def add_goods(request,openid,store_id):
    """
    :request method: POST
    :param openid: 用户唯一id（无需上传）
    :param goods_url: 商品链接(必填)
    :param pic_path: 图片路径(必填)
    :param brand: 商品品牌(必填)
    :param goods_name: 商品名称(必填)
    :param specification: 规格(必填)
    :param storage_condition: 存储条件(必填)
    :param shelf_life: 保质期(必填)
    :param unsuitable_people: 不适用人群(必填)
    :param favorable_rate: 好评率(必填)
    :param selling_point: 卖点
    :param live_recording_screen_path: 其他主播直播录屏
    :param daily_price: 日常价格
    :param lowest_price: 历史最低价
    :param tmall_price: 天猫价格
    :param taobao_price: 淘宝价格
    :param other_price: 其他平台价格
    :param live_price: 直播价格
    :param preferential_way: 直播优惠方式
    :param delivery_company: 快递公司
    :param shipping_addresses: 发货地址
    :param shipping_cycle: 发货周期
    :param free_shipping: 包邮地区
    :param not_shipping: 不发货区域
    :param comment: 备注信息
    :param store_id: 商铺id(必填)
    :return:
    """
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '添加商品失败'}

    try:
        _, data = get_store_data_by_store_id(openid, store_id)
        if not data:
            raise InvalidParameter('店铺不存在')

        is_success,pk = insert_goods_data(openid,json.loads(request.body))
        if is_success:
            rsp = {'code': ResponsCode.SUCCESS, 'data': {"goods_id":pk},"msg":'添加商品成功'}
    except InvalidParameter as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '',"msg":'添加商品异常'}
    finally:
        return rsp



@json_response
@get_params
def update_goods(request,openid,goods_id,store_id):
    """
    :request method: POST
    :param openid: 用户唯一id（无需上传）
    :param goods_url: 商品链接
    :param pic_path: 图片路径
    :param live_recording_screen_path: 其他主播直播录屏
    :param brand: 商品品牌
    :param goods_name: 商品名称
    :param specification: 规格
    :param selling_point: 卖点
    :param storage_condition: 存储条件
    :param shelf_life: 保质期
    :param unsuitable_people: 不适用人群
    :param favorable_rate: 好评率
    :param daily_price: 日常价格
    :param lowest_price: 历史最低价
    :param tmall_price: 天猫价格
    :param taobao_price: 淘宝价格
    :param other_price: 其他平台价格
    :param live_price: 直播价格
    :param preferential_way: 直播优惠方式
    :param delivery_company: 快递公司
    :param shipping_addresses: 发货地址
    :param shipping_cycle: 发货周期
    :param free_shipping: 包邮地区
    :param not_shipping: 不发货区域
    :param comment: 备注信息
    :param store_id: 商铺id(必填)
    :param goods_id: 商品id(必填)
    :return:
    """
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '更新商品失败'}

    try:
        _, data = get_store_data_by_store_id(openid, store_id)
        if not data:
            raise InvalidParameter('店铺不存在')
        is_success = update_goods_data_by_id(openid,goods_id,json.loads(request.body))
        if is_success:
            rsp = {'code': ResponsCode.SUCCESS, 'data': '',"msg":'更新商品成功'}
    except InvalidParameter as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '',"msg":'更新商品异常'}
    finally:
        return rsp

@json_response
@get_params
def get_goods_info(request,openid,goods_id=None):
    """
    :request method: POST
    :param openid: 用户唯一id（无需上传）
    :param goods_id: 商品id
    :return:
    """
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '获取商品失败'}
    try:
        is_success,all_goods = get_goods_data(openid,goods_id)
        if is_success:
            rsp = {'code': ResponsCode.SUCCESS, 'data':all_goods,"msg":'获取商品成功'}
    except InvalidParameter as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '',"msg":'获取商品异常'}
    finally:
        return rsp


@json_response
@get_params
def get_store_goods_info(request,openid,store_id):
    """
    :request method: POST
    :param openid: 用户唯一id（无需上传）
    :store_id: 商铺ID
    :return:
    """
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '获取商品失败'}
    try:
        is_success,all_goods = get_store_goods_data(openid,store_id)
        if is_success:
            rsp = {'code': ResponsCode.SUCCESS, 'data':all_goods,"msg":'获取商品成功'}
    except InvalidParameter as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '',"msg":'获取商品异常'}
    finally:
        return rsp