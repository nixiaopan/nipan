# -*- coding: utf-8 -*-
'''
@author: nixiaopan
@time: 2022/3/30 22:25
'''
class ResponsCode:
    """0 成功 1 失败 2 异常"""
    SUCCESS = 200
    FAILED = 450
    EXCEPTION = 550

class IdentityType:
    ANCHOR = 1
    BUSINESSES = 2

class CooperationStatus:
    UNSENT_COOPERATION = 0
    WAITING_FOR_ANCHOR_GET_SAMPLE = 1
    WAITING_FOR_MERCHANT_SEND_SAMPLE = 2
    WAITING_FOR_ANCHOR_TEST_SAMPLE = 3
    SAMPLE_TEST_END = 4

class SampleTestStatus:
    NO_TEST = 0
    SUCESS = 1
    FAILED = 2