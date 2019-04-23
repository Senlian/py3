#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config.aliyun_metrics import AliyunMetrics

AliyunAccessKeyID = 'ak'
AliyunAccessKeySecret = 'secret'
AliyunRegionID = 'cn-hangzhou'
AliyunProject = 'acs_ecs_dashboard'
# 设置返回格式,JSON/XML,默认XML
AliyunDataFormate = 'JSON'
AliyunDomain = 'metrics.cn-hangzhou.aliyuncs.com'
AliyunHosts = [
    {'name': 'ServerName1', 'host': 'IP1', 'Dimensions': {'instanceId': 'i-xxxxxxxx'}},
    {'name': 'ServerName2', 'host': 'IP2', 'Dimensions': {'instanceId': 'i-xxxxxxxx'}},
    {'name': 'ServerName3', 'host': 'IP3', 'Dimensions': {'instanceId': 'i-xxxxxxxx'}},
]

AliyunMetrics = AliyunMetrics()
