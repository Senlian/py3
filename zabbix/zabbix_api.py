#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import requests
from config.settings import settings
from graph.graph import Graph


# http://www.zabbix.com/documentation/3.4/zh/manual/api/reference/history/get
def aver(item):
    return sum(item) / len(item) if len(item) > 0 else 0


class ZabbixApi(object):
    def __init__(self):
        self.token = self.authenticate()

    def request(self, data):
        request = requests.post(url=settings.ZabbixUri, headers=settings.ZabbixHeaders, data=json.dumps(data))
        response = json.loads(request.text)
        request.close()
        if response.get("error"):
            return response.get("error")
        else:
            return response.get("result")

    def authenticate(self):
        '''
            :desc: 用户身份验证
            :return: token
        '''
        data = {
            "jsonrpc": settings.ZabbixJsonrpc,
            "method": "user.login",
            "params": {
                "user": settings.ZabbixUser,
                "password": settings.ZabbixPassword
            },
            "id": 1,
            "auth": None
        }
        return self.request(data)

    def host_list(self, search=None) -> dict:
        '''
            :desc: 获取主机列表
            :return: list
        '''
        data = {
            "jsonrpc": settings.ZabbixJsonrpc,
            "method": "host.get",
            "params": {
                "output": ["hostid", "host"],
                "selectInterfaces": ["ip"],
                "search": search
            },
            "id": 2,
            "auth": self.token
        }
        return self.request(data)

    def metric_list(self, host_id, search=None):
        data = {
            "jsonrpc": settings.ZabbixJsonrpc,
            "method": "item.get",
            "params": {
                "output": ["hostid", "itemid", "name", "key_"],
                "hostids": host_id,
                "sortfield": "itemid",
                "search": search
            },
            "auth": self.token,
            "id": 1
        }
        return self.request(data)

    def metric_data(self, itemid, history=3):
        data = {
            "jsonrpc": settings.ZabbixJsonrpc,
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": history,
                "itemids": itemid,
                "sortfield": "clock",
                "sortorder": "DESC",
                "time_from": settings.strptime(settings.StartTime, settings.TimeFormat),
                "time_till": settings.strptime(settings.EndTime, settings.TimeFormat)
            },
            "auth": self.token,
            "id": 1
        }
        return self.request(data)

    def get_values(self, datas):
        return [float(data.get('value')) for data in datas]

    def get_values_with_stamp(self, datas, rate=1, format='%Y-%m-%d %H:%M:%S'):
        return sorted([(settings.numpytime(int(data.get('clock'))), float(data.get('value')) / rate) for data in datas],
                      key=lambda x: x[0])

    def maxtime(self, datas):
        maximum = max(self.get_values(datas))
        return [settings.strftime(int(data.get('clock'))) for data in datas if float(data.get('value')) >= maximum]

    def deal_with_query(self, hostid, key, rate=1, name=None, unit=None):
        if key:
            metrics = self.metric_list(hostid, search={"key_": key})
            if metrics:
                metric = metrics[0]
                itemid = metric.get('itemid')
                datas = self.metric_data(itemid) or self.metric_data(itemid, 0)
                metric_data = self.get_values(datas)
                if datas:
                    minimum = round(min(metric_data) / rate, 2)
                    average = round(aver(metric_data) / rate, 2)
                    maximum = round(max(metric_data) / rate, 2)
                    maxtimes = len(self.maxtime(datas))
                    graph = Graph(average=settings.get_ndarry(self.get_values_with_stamp(datas, rate)),
                                  title=name, subtitle=True, unit=unit)
                    graphs = graph()
                    return minimum, average, maximum, maxtimes, graphs


def query_host_data(host=None):
    if not host:
        return None
    api = ZabbixApi()
    host = api.host_list(search={'host': host})[0]
    hostid = host.get('hostid', '')
    if not hostid:
        return None
    for monitor in settings.ZabbixMonitorKeys:
        name = monitor.get('name')
        key = monitor.get('metric', None)
        unit = monitor.get('unit', 1)
        rate = monitor.get('rate', 1)
        yield name, api.deal_with_query(hostid, key, rate, name, unit)


if __name__ == '__main__':
    api = ZabbixApi()

    datas = api.deal_with_query('10260', 'get.monitor.info[sswap_used,os]', 1)
    # for data in datas:
    print(datas)
