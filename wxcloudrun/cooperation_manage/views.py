import traceback
import json
from wxcloudrun.utils.SQL.DBUtils import DBUtils
from wxcloudrun.utils.exception import PreconditionErr
from wxcloudrun.utils.logger import logger
from wxcloudrun.commons.constant import ResponsCode, IdentityType, CooperationStatus, SampleTestStatus
from wxcloudrun.mapper.cooperation import insert_cooperation_data, update_cooperation_data, \
    update_cooperation_status, get_cooperation_status_for_update, get_cooperation_data_for_update, \
    update_cooperation_status_and_set_sample_courier_number, update_cooperation_status_and_set_shipping_info, \
    update_cooperation_status_and_set_test_result, get_cooperation_data_by_status
from wxcloudrun.mapper.user_info import get_user_data
from wxcloudrun.utils.decorators import get_params, json_response


def identity_check(openid, identity):
    is_success, user_data = get_user_data(openid)
    if not user_data:
        return False
    if user_data[0].get("identity_type") == identity:
        return True
    else:
        return False


@json_response
@get_params
def new_cooperation(request, openid, store_id, store_name, dsr,
                    goods_id, goods_name, specification, brand, favorable_rate, pic_path, live_recording_screen_path,
                    daily_price, live_price, commission_rate, pos_price, preferential_way, goods_url, hand_card,
                    storage_condition, shelf_life, unsuitable_people, ability_to_deliver, shipping_cycle,
                    shipping_addresses,
                    delivery_company, not_shipping):
    """
    新建一次合作
    :request method: POST
    以下所有必填，没有填“无”
    商铺信息
    :param store_id: 店铺id(最长45位)
    :param store_name: 店铺id(最长45位)
    :param dsr: 店铺评分
    商品信息
    :param goods_id: 商品id
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
    {'code': ResponsCode.FAILED, 'data': '', "msg": '新建合作单失败'}
    {'code': ResponsCode.SUCCESS, 'data': {"cooperation_id":pk},"msg":'新建合作单成功'}
    {'code': ResponsCode.EXCEPTION, 'data': '',"msg":'新建合作单异常'}
    :Example：
    {
    "goods_url":"https://item.jd.com/100030291368.html",
    "pic_path":["https://img30.360buyimg.com/sku/jfs/t1/200456/25/20481/184777/61b8a292E325a6ca9/79021d299865b2b9.jpg"],
    "live_recording_screen_path":"https://jvod.300hu.com/vod/product/5c59e1dd-5ef4-4046-995a-88d4e73653b9/eb7adb4d179443c09c91953b65108a08.mp4?source=2&h265=h265/18799/6281e15a04d443c38b3392427d62a6b4.mp4",
    "brand":"MC",
    "goods_name":"T5真无线蓝牙耳机降噪双耳入耳式运动跑步迷你隐形游戏通用于华为苹果vivo小米oppo荣耀手机 迈从T5尊贵黑（智能数显/高清镜面/9D音效）",
    "specification":"240g（16包左右）包邮",
    "hand_card":"十三香虾尾优势： 1.方便快捷，开盖换碗加热即食 2.多种搭配（可做虾尾拌面/加入喜欢的蔬菜做炒菜/虾尾火鸡面等） 3.高标准严格清洗，整洁卫生，无需二次清理 4.肉质紧实，颗颗饱满 5.数十种香料秘制，汤汁爽辣，浓香四溢 6.人工筛选新鲜活虾，人工取尾，虾尾饱满q弹",
    "storage_condition":"低温冷冻保存",
    "shelf_life":"12",
    "unsuitable_people":"老少皆宜",
    "favorable_rate":"95.6",
    "daily_price":"19.9/10包 29.8/15包 39.9/24包 49.9/30包",
    "lowest_price":"19.9/10包 29.8/15包 39.9/24包 49.9/30包",
    "tmall_price":"",
    "taobao_price":"",
    "other_price":"",
    "live_price":"19.9/10包 29.8/15包 39.9/24包 49.9/30包",
    "preferential_way":"限时秒杀",
    "delivery_company":"物流公司：百世  中通  邮政  韵达  圆通，不接受指定快递",
    "shipping_addresses":"安徽合肥",
    "shipping_cycle":"现货48小时发出，预售7天内",
    "free_shipping":"江浙沪",
    "not_shipping":"无",
    "comment":"",
    "store_id":"22222245",
    "goods_id":8,
    "anchor_openid":"oJ92T5adaBqYeg9lC_9ouxHKoHfQ",
    "commission_rate":"3.5",
    "pos_price":"5000",
    "store_name":"倪攀的小店@#￥#@#",
    "dsr":"12",
    "ability_to_deliver":999
    }
    """
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '新建合作单失败'}
    try:
        if not identity_check(openid, IdentityType.BUSINESSES):
            raise PreconditionErr("只有商家才能新建合作单")
        is_success, pk = insert_cooperation_data(openid, json.loads(request.body))
        if is_success:
            rsp = {'code': ResponsCode.SUCCESS, 'data': {"cooperation_id": pk}, "msg": '新建合作单成功'}
    except PreconditionErr as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '新建合作单异常'}
    finally:
        return rsp


@json_response
@get_params
def update_cooperation_info(request, openid, cooperation_id):
    """
    更新合作信息，只有在未发送申请的阶段，才能修改
    :paran cooperation_id:合作单id
    商铺信息
    :param store_id: 店铺id(最长45位)
    :param store_name: 店铺id(最长45位)
    :param dsr: 店铺评分
    商品信息
    :param goods_id: 商品id
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
   {'code': ResponsCode.FAILED, 'data': '', "msg": '修改合作单失败'}
   {'code': ResponsCode.FAILED, 'data': '', "msg": '合作单不存在'}
   {'code': ResponsCode.FAILED, 'data': '', "msg": '合作单已发送，无法修改'}
   {'code': ResponsCode.FAILED, 'data': '', "msg": '合作人身份类型错误'}
   {'code': ResponsCode.FAILED, 'data': '', "msg": '合作单修改成功'}
   {'code': ResponsCode.FAILED, 'data': '', "msg": '合作单修改异常'}
   :Example:
   {
    "goods_url":"https://item.jd.com/100030291368.html",
    "pic_path":"https://img30.360buyimg.com/sku/jfs/t1/200456/25/20481/184777/61b8a292E325a6ca9/79021d299865b2b9.jpg",
    "live_recording_screen_path":"https://jvod.300hu.com/vod/product/5c59e1dd-5ef4-4046-995a-88d4e73653b9/eb7adb4d179443c09c91953b65108a08.mp4?source=2&h265=h265/18799/6281e15a04d443c38b3392427d62a6b4.mp4",
    "brand":"MC",
    "goods_name":"T5真无线蓝牙耳机降噪双耳入耳式运动跑步迷你隐形游戏通用于华为苹果vivo小米oppo荣耀手机 迈从T5尊贵黑（智能数显/高清镜面/9D音效）",
    "specification":"240g（16包左右）包邮",
    "selling_point":"十三香虾尾优势： 1.方便快捷，开盖换碗加热即食 2.多种搭配（可做虾尾拌面/加入喜欢的蔬菜做炒菜/虾尾火鸡面等） 3.高标准严格清洗，整洁卫生，无需二次清理 4.肉质紧实，颗颗饱满 5.数十种香料秘制，汤汁爽辣，浓香四溢 6.人工筛选新鲜活虾，人工取尾，虾尾饱满q弹",
    "storage_condition":"低温冷冻保存",
    "shelf_life":"12",
    "unsuitable_people":"老少皆宜",
    "favorable_rate":"95.6",
    "daily_price":"19.9/10包 29.8/15包 39.9/24包 49.9/30包",
    "lowest_price":"19.9/10包 29.8/15包 39.9/24包 49.9/30包",
    "tmall_price":"",
    "taobao_price":"",
    "other_price":"",
    "live_price":"19.9/10包 29.8/15包 39.9/24包 49.9/30包",
    "preferential_way":"限时秒杀",
    "delivery_company":"物流公司：百世  中通  邮政  韵达  圆通，不接受指定快递",
    "shipping_addresses":"安徽合肥",
    "shipping_cycle":"现货48小时发出，预售7天内",
    "free_shipping":"江浙沪",
    "not_shipping":"无",
    "comment":"",
    "store_id":"22222245",
    "goods_id":8,
    "commission_rate":"35.5",
    "pos_price":"5000",
    "store_name":"倪攀",
    "dsr":"12",
    "cooperation_id":"1"
    }
   """
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '修改合作单失败'}

    try:
        if not identity_check(openid, IdentityType.BUSINESSES):
            raise PreconditionErr("只有商家才能修改合作单")
        cur_db_util = DBUtils()
        with cur_db_util.transcontext(True):
            data = get_cooperation_status_for_update(cooperation_id, cur_db_util)
            if not data:
                raise PreconditionErr("合作单不存在")
            else:
                if data[0].get("status") != CooperationStatus.UNSENT_COOPERATION:
                    raise PreconditionErr("合作单已发送，无法修改")

            # print(cur_db_util.execute_single_sql_in_transaction('''update  cooperation set dsr="100" where id = "33"'''))
            update_cooperation_data(cooperation_id, cur_db_util, json.loads(request.body))
            rsp = {'code': ResponsCode.SUCCESS, 'data': '', "msg": '合作单修改成功'}
    except PreconditionErr as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        # logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '合作单修改异常'}
    finally:
        return rsp


@json_response
@get_params
def send_apply(request, openid, cooperation_id, anchor_openid):
    """
    商家才能发送申请，请求合作
    :request method: POST
    :param cooperation_id: 合作id
    :param anchor_openid:主播id
    :return:
    {'code': ResponsCode.FAILED, 'data': '', "msg": '合作申请发送失败'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '只有商家才能发送申请'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '发送对象不是主播'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '合作单不存在'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '合作单已发送，请勿重复发送'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '身份错误，无权限发送申请'}
    {'code': ResponsCode.SUCCESS, 'data': '',"msg":'合作申请发送成功，等待主播申请领样'}
    {'code': ResponsCode.EXCEPTION, 'data': '',"msg":'合作申请发送异常，请稍后再试'}
    :Example:
    {
    "cooperation_id":"32",
    "anchor_openid":"oJ92T5SVgfc_sth2uF0ObS1hEEIQ"
    }
    """
    # openid = "oJ92T5adaBqYeg9lC_9ouxHKoHfQ"
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '合作申请发送失败'}
    try:
        # if not identity_check(openid, IdentityType.BUSINESSES):
        #     raise PreconditionErr("只有商家才能发送申请")
        if not identity_check(anchor_openid, IdentityType.ANCHOR):
            raise PreconditionErr("发送对象不是主播")
        cur_db_util = DBUtils()
        with cur_db_util.transcontext(True):
            data = get_cooperation_data_for_update(cooperation_id, cur_db_util)
            if not data:
                raise PreconditionErr('合作单不存在')
            else:
                if data[0].get("status") != CooperationStatus.UNSENT_COOPERATION:
                    raise PreconditionErr("合作单已发送，请勿重复发送")
                if data[0].get("merchant_openid") != openid:
                    raise PreconditionErr("身份错误，无权限发送申请")
            update_cooperation_status(cooperation_id, anchor_openid, CooperationStatus.WAITING_FOR_ANCHOR_GET_SAMPLE,
                                      CooperationStatus.UNSENT_COOPERATION, cur_db_util)
            rsp = {'code': ResponsCode.SUCCESS, 'data': '', "msg": '合作申请发送成功，等待主播申请领样'}
    except PreconditionErr as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '合作申请发送异常，请稍后再试'}
    finally:
        return rsp


@json_response
@get_params
def apply_for_sample(request, openid, cooperation_id, anchor_name, anchor_phone_number, anchor_shipping_address,
                     sample_count, sample_comment):
    """
    主播才能发送申请领取样品
    :request method: POST
    :param cooperation_id: 合作id
    :param anchor_name: 主播姓名
    :param anchor_phone_number: 主播手机号
    :param anchor_shipping_address: 主播收货地址
    :param sample_count: 样品个数
    :param sample_comment: 其他要求
    :return:
    {'code': ResponsCode.FAILED, 'data': '', "msg": '领样申请发送失败'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '只有主播才能发送领样申请'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '合作单不存在'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '不在申请领样阶段，无法申请领样'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '身份错误，无权限发送领样申请'}
    {'code': ResponsCode.SUCCESS, 'data': '',"msg":'领样申请发送成功，等待商家发送样品'}
    {'code': ResponsCode.EXCEPTION, 'data': '',"msg":'领样申请发送异常，请稍后再试'}
    :Exampl:
    {
    "cooperation_id":"1",
    "anchor_shipping_address":"浙江省杭州市11111111区",
    "anchor_phone_number":"13777861401",
    "anchor_name":"倪攀",
    "sample_count":1,
    "sample_comment":"333"
    }
    """
    # openid = "oJ92T5adaBqYeg9lC_9ouxHKoHfQ"
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '领样申请发送失败'}
    try:
        if not identity_check(openid, IdentityType.ANCHOR):
            raise PreconditionErr("只有主播才能发送领样申请")
        cur_db_util = DBUtils()
        with cur_db_util.transcontext(True):
            data = get_cooperation_data_for_update(cooperation_id, cur_db_util)
            if not data:
                raise PreconditionErr('合作单不存在')
            else:
                if data[0].get("status") != CooperationStatus.WAITING_FOR_ANCHOR_GET_SAMPLE:
                    raise PreconditionErr("不在申请领样阶段，无法申请领样")
                if data[0].get("anchor_openid") != openid:
                    raise PreconditionErr("身份错误，无权限发送领样申请")

            update_cooperation_status_and_set_shipping_info(cooperation_id,
                                                            CooperationStatus.WAITING_FOR_MERCHANT_SEND_SAMPLE,
                                                            CooperationStatus.WAITING_FOR_ANCHOR_GET_SAMPLE,
                                                            anchor_shipping_address, anchor_phone_number,
                                                            anchor_name, sample_count, sample_comment, cur_db_util)
            rsp = {'code': ResponsCode.SUCCESS, 'data': '', "msg": '领样申请发送成功，等待商家发送样品'}
    except PreconditionErr as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '领样申请发送异常，请稍后再试'}
    finally:
        return rsp


@json_response
@get_params
def send_sample(request, openid, cooperation_id, sample_courier_number):
    """
    主播才能发送申请领取样品
    :request method: POST
    :param cooperation_id: 合作id
    :param sample_courier_number: 快递单号
    :return:
    {'code': ResponsCode.FAILED, 'data': '', "msg": '发送样品失败'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '只有商家才能发送样品'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '合作单不存在'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '不在发送样品阶段，无法发送样品领样'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '身份错误，无权限发送领样申请'}
    {'code': ResponsCode.SUCCESS, 'data': '',"msg":'样品发送成功，等待主播试样'}
    {'code': ResponsCode.EXCEPTION, 'data': '',"msg":'发送样品异常，请稍后再试'}
    :Example:
    {
    "cooperation_id":"1",
    "sample_courier_number":"4654654654965465465"
    }
    """
    # openid = "oJ92T5adaBqYeg9lC_9ouxHKoHfQ"
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '发送样品失败'}
    try:
        if not identity_check(openid, IdentityType.BUSINESSES):
            raise PreconditionErr("只有商家才能发送样品")
        cur_db_util = DBUtils()
        with cur_db_util.transcontext(True):
            data = get_cooperation_data_for_update(cooperation_id, cur_db_util)
            if not data:
                raise PreconditionErr('合作单不存在')
            else:
                if data[0].get("status") != CooperationStatus.WAITING_FOR_MERCHANT_SEND_SAMPLE:
                    raise PreconditionErr("不在发送样品阶段，无法发送样品领样")
                if data[0].get("merchant_openid") != openid:
                    raise PreconditionErr("身份错误，无权限发送领样申请")

            update_cooperation_status_and_set_sample_courier_number(cooperation_id,
                                                                    CooperationStatus.WAITING_FOR_ANCHOR_TEST_SAMPLE,
                                                                    CooperationStatus.WAITING_FOR_MERCHANT_SEND_SAMPLE,
                                                                    sample_courier_number, cur_db_util)
            rsp = {'code': ResponsCode.SUCCESS, 'data': '', "msg": '样品发送成功，等待主播试样'}
    except PreconditionErr as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '发送样品异常，请稍后再试'}
    finally:
        return rsp


@json_response
@get_params
def test_sample(request, openid, cooperation_id, test_result, test_failed_reason=None, test_comment=None):
    """
    试样：主播才能试样
    :request method: POST
    :param cooperation_id: 合作id
    :param test_result: 试样结果0未试样，1试样通过，2试样不通过
    :param test_failed_reason: 测试不通过原因
    :param test_comment: 测试结果说明（失败请填写备注）
    :return:
    {'code': ResponsCode.FAILED, 'data': '', "msg": '试样结果填写失败'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '只有主播才能试样'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '合作单不存在'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '不在试样阶段，无法填写试样结果'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '身份错误，无法填写试样结果'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '没有测试结果，请填写之后上传'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '测试不通过，请填写原因'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '测试状态错误'}
    {'code': ResponsCode.SUCCESS, 'data': '',"msg":'试样结果填写成功，合作完成'}
    {'code': ResponsCode.EXCEPTION, 'data': '',"msg":'试样结果填写异常，请稍后再试'}
    :Example:
    {
    "cooperation_id":"1",
    "test_result":"2",
    "test_comment":"太辣鸡了",
    "test_failed_reason":"其他"
}
    """
    # openid = "oJ92T5adaBqYeg9lC_9ouxHKoHfQ"
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '试样结果填写失败'}
    try:
        if not identity_check(openid, IdentityType.ANCHOR):
            raise PreconditionErr("只有主播才能试样")
        cur_db_util = DBUtils()
        with cur_db_util.transcontext(True):
            data = get_cooperation_data_for_update(cooperation_id, cur_db_util)
            if not data:
                raise PreconditionErr('合作单不存在')
            else:
                if data[0].get("status") != CooperationStatus.WAITING_FOR_ANCHOR_TEST_SAMPLE:
                    raise PreconditionErr("不在试样阶段，无法填写试样结果")
                if data[0].get("anchor_openid") != openid:
                    raise PreconditionErr("身份错误，无法填写试样结果")
            test_result = int(test_result)
            if test_result == SampleTestStatus.NO_TEST:
                raise PreconditionErr("没有测试结果，请填写之后上传")
            elif test_result == SampleTestStatus.FAILED:
                print(test_comment, type(test_comment))
                if not test_comment:
                    raise PreconditionErr("测试不通过，请填写原因")
            elif test_result == SampleTestStatus.SUCESS:
                pass
            else:
                raise PreconditionErr("测试状态错误")
            update_cooperation_status_and_set_test_result(cooperation_id, CooperationStatus.SAMPLE_TEST_END,
                                                          CooperationStatus.WAITING_FOR_ANCHOR_TEST_SAMPLE, test_result,
                                                          test_failed_reason, test_comment, cur_db_util)
            rsp = {'code': ResponsCode.SUCCESS, 'data': '', "msg": '试样结果填写成功，合作完成'}
    except PreconditionErr as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '试样结果填写异常，请稍后再试'}
    finally:
        return rsp


@json_response
@get_params
def get_cooperation_info_by_status_and_test_result(request, openid, status, page_number, count, test_result=None):
    """
    根据合作单状态和试样结果获取合作单信息
    :request method: POST
    :param status: 0未发送，1等待主播申请获取样品，2等待商家发送样品，3等待主播试样，4试样结束
    :param page_number: 当前是第几页
    :param count: 一页需要多少个数据
    :param test_result: 试样结果0未试样，1试样通过，2试样不通过
    :return:
    {'code': ResponsCode.FAILED, 'data': '', "msg": '获取合作单失败'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '无法获取用户信息'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '用户身份错误'}
    {'code': ResponsCode.SUCCESS, 'data': '', "msg": '获取合作单成功'}
    {'code': ResponsCode.FAILED, 'data': '', "msg": '获取合作单异常，请稍后再试'}
    :Example:
    {
    "status":1,
    "test_result":0
    }
    """
    rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": '获取合作单失败'}
    try:
        is_success, user_data = get_user_data(openid)
        if not user_data:
            raise PreconditionErr("无法获取用户信息")
        identity_type = user_data[0].get("identity_type")
        start = (int(page_number) - 1) * int(count)
        print(openid, status, page_number, count, test_result, type(test_result))
        if identity_type == IdentityType.ANCHOR:
            cooperation_data = get_cooperation_data_by_status(status, openid, "anchor_openid", test_result, start,
                                                              count)
        elif identity_type == IdentityType.BUSINESSES:
            cooperation_data = get_cooperation_data_by_status(status, openid, "merchant_openid", test_result, start,
                                                              count)
        else:
            raise PreconditionErr("用户身份错误")

        rsp = {'code': ResponsCode.SUCCESS, 'data': cooperation_data, "msg": '获取合作单成功'}
    except PreconditionErr as e:
        rsp = {'code': ResponsCode.FAILED, 'data': '', "msg": str(e)}
    except:
        logger.exception(traceback.format_exc())
        rsp = {'code': ResponsCode.EXCEPTION, 'data': '', "msg": '获取合作单异常，请稍后再试'}
    finally:
        return rsp
