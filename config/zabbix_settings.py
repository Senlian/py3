#!/usr/bin/env python3
# -*- coding: utf-8 -*-

ZabbixUri = 'http://domain/api_jsonrpc.php'
ZabbixUser = 'username'
ZabbixPassword = 'password'
ZabbixHeaders = {"Content-Type": "application/json-rpc"}

ZabbixJsonrpc = '2.0'

ZabbixMonitorKeys = [
    {'name': 'CPU使用率(%)', 'metric': 'perf_counter[\Processor(_Total)\% Processor Time]', 'unit': '%%', 'rate': 1},
    {'name': '内存使用率(%)', 'metric': 'get.process.info[mem_usd]', 'unit': '%%', 'rate': 1},
    {'name': 'VMS使用值(GB)', 'metric': 'get.monitor.info[sswap_used,os]', 'unit': 'GB', 'rate': 1024 * 1024 * 1024},
    {'name': 'VMS使用值(GB)', 'metric': 'get.process.info[vms_used,,]', 'unit': 'GB', 'rate': 1024 * 1024 * 1024},

    {'name': 'SqlServer CPU使用率(%)', 'metric': 'get.monitor.info[pcpu_percent,sqlservr.exe]', 'unit': '%%', 'rate': 1},
    {'name': 'SqlServer VMS使用值(GB)', 'metric': 'get.monitor.info[pvms,sqlservr.exe,,]', 'unit': 'GB',
     'rate': 1024 * 1024 * 1024},

    {'name': '7800节点内存峰值(GB)', 'metric': 'get.redis.info[127.0.0.1,7800,MemoryPeak]', 'unit': 'GB',
     'rate': 1024 * 1024 * 1024},

    {'name': '7801节点内存峰值(GB)', 'metric': 'get.redis.info[127.0.0.1,7801,MemoryPeak]', 'unit': 'GB',
     'rate': 1024 * 1024 * 1024},

    {'name': '7802节点内存峰值(GB)', 'metric': 'get.redis.info[127.0.0.1,7802,MemoryPeak]', 'unit': 'GB',
     'rate': 1024 * 1024 * 1024},

    {'name': '7800数据量(条)', 'metric': 'get.redis.info[127.0.0.1,7800,KeySize]', 'unit': None, 'rate': 1},
    {'name': '7801数据量(条)', 'metric': 'get.redis.info[127.0.0.1,7801,KeySize]', 'unit': None, 'rate': 1},
    {'name': '7802数据量(条)', 'metric': 'get.redis.info[127.0.0.1,7802,KeySize]', 'unit': None, 'rate': 1},

    {'name': '7800慢查询(条)', 'metric': 'get.redis.info[127.0.0.1,7800,SlowLogSize]', 'unit': None, 'rate': 1},
    {'name': '7801慢查询(条)', 'metric': 'get.redis.info[127.0.0.1,7801,SlowLogSize]', 'unit': None, 'rate': 1},
    {'name': '7802慢查询(条)', 'metric': 'get.redis.info[127.0.0.1,7802,SlowLogSize]', 'unit': None, 'rate': 1},
]
