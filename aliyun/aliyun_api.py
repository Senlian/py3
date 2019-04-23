#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, time
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcms.request.v20180308 import QueryMetricListRequest

from config.settings import settings
from graph.graph import Graph


def formate_time(ftime, formate='%Y-%m-%d %H:%M:%S'):
    return time.strftime(formate, time.localtime(ftime))


def aver(item):
    return sum(item) / len(item) if len(item) > 0 else 0


class AliyunApi(object):
    def __init__(self, Dimensions=None):
        if not Dimensions:
            raise ValueError('无效的阿里云实例ID')
        # {'instanceId': 'i-2ze9g61a1atwhvmi05l4'}
        self.Dimensions = Dimensions
        self.asc_client = AcsClient(ak=settings.AliyunAccessKeyID,
                                    secret=settings.AliyunAccessKeySecret,
                                    region_id=settings.AliyunRegionID)

    def requset(self, metric, cursor=None):
        cms_request = QueryMetricListRequest.QueryMetricListRequest()
        # _request.set_action_name("QueryMetricList")
        # 设置返回格式,JSON/XML,默认XML
        cms_request.set_accept_format(settings.AliyunDataFormate)
        cms_request.set_Project(settings.AliyunProject)
        cms_request.set_Dimensions(Dimensions=self.Dimensions)
        cms_request.set_Period(settings.Period)
        cms_request.set_Metric(metric)
        cms_request.set_StartTime(settings.StartTime)
        cms_request.set_EndTime(settings.EndTime)
        if cursor:
            cms_request.set_Cursor(cursor)
            cms_request.set_Length(min(1440 / self.period * 60, 1000))
        return cms_request

    def query(self, metric, cursor=None) -> dict:
        if not metric:
            return {}
        cms_request = self.requset(metric, cursor)
        datas = json.loads(self.asc_client.do_action_with_exception(cms_request))
        # print(json.dumps(datas, indent=2),file= open('test.json','w'))
        return json.loads(datas.get('Datapoints', {}))

    def max(self, datas):
        return max([data.get('Maximum', 0) for data in datas])

    def min(self, datas):
        return min([data.get('Minimum', 0) for data in datas])

    def aver(self, datas):
        return aver([data.get('Average', 0) for data in datas])

    def maxtime(self, datas):
        maximum = self.max(datas)
        return [formate_time(data.get('timestamp', 0) / 1000) for data in datas if
                data.get('Maximum', 0) >= maximum]

    def deal_with_timestamp(self, datas, rate):
        minimum = (
            [(settings.numpytime(data.get('timestamp', 0) / 1000), data.get('Minimum', 0) / rate) for data in datas])
        average = (
            [(settings.numpytime(data.get('timestamp', 0) / 1000), data.get('Average', 0) / rate) for data in datas])
        maximum = (
            [(settings.numpytime(data.get('timestamp', 0) / 1000), data.get('Maximum', 0) / rate) for data in datas])

        return minimum, average, maximum
        # return average

    def deal_with_query(self, name=None, unit=None, metric=None, rate=1, cursor=None):
        if not metric:
            return None
        data_points = self.query(metric, cursor)
        if not data_points:
            return None
        datas = [data for data in data_points if
                 ('state' not in data)
                 or ('device' not in data)
                 or (data.get('state', None) == 'TCP_TOTAL')
                 or (data.get('device', None) in ['C:\\', 'D:\\', 'E:\\', '/dev/vdb1'])]

        minimum = []
        average = []
        maximum = []
        maxtimes = []
        graphs = []
        if metric.startswith('disk'):
            disk_c_data = [data for data in datas if data.get('device', None) == 'C:\\']
            disk_d_data = [data for data in datas if data.get('device', None) == 'D:\\']
            disk_e_data = [data for data in datas if data.get('device', None) == 'E:\\']
            disk_home_data = [data for data in datas if data.get('device', None) == '/dev/vdb1']
            if disk_c_data:
                minimum.append({'C盘': round(self.min(disk_c_data) / rate, 2)})
                average.append({'C盘': round(self.aver(disk_c_data) / rate, 2)})
                maximum.append({'C盘': round(self.max(disk_c_data) / rate, 2)})
                maxtimes.append({'C盘': len(self.maxtime(disk_c_data))})

                minimum_datas, average_datas, maximum_datas = self.deal_with_timestamp(disk_c_data, rate)
                graph = Graph(minimum=settings.get_ndarry(minimum_datas),
                              average=settings.get_ndarry(average_datas),
                              maximum=settings.get_ndarry(maximum_datas),
                              title='C盘' + name, subtitle=True, unit=unit)()
                graphs.append({'C盘': graph})

            if disk_d_data:
                minimum.append({'D盘': round(self.min(disk_d_data) / rate, 2)})
                average.append({'D盘': round(self.aver(disk_d_data) / rate, 2)})
                maximum.append({'D盘': round(self.max(disk_d_data) / rate, 2)})
                maxtimes.append({'D盘': len(self.maxtime(disk_d_data))})
                minimum_datas, average_datas, maximum_datas = self.deal_with_timestamp(disk_d_data, rate)
                graph = Graph(minimum=settings.get_ndarry(minimum_datas),
                              average=settings.get_ndarry(average_datas),
                              maximum=settings.get_ndarry(maximum_datas),
                              title='D盘' + name, subtitle=True, unit=unit)()
                graphs.append({'D盘': graph})

            if disk_e_data:
                minimum.append({'E盘': round(self.min(disk_e_data) / rate, 2)})
                average.append({'E盘': round(self.aver(disk_e_data) / rate, 2)})
                maximum.append({'E盘': round(self.max(disk_e_data) / rate, 2)})
                maxtimes.append({'E盘': len(self.maxtime(disk_e_data))})
                minimum_datas, average_datas, maximum_datas = self.deal_with_timestamp(disk_e_data, rate)
                graph = Graph(minimum=settings.get_ndarry(minimum_datas),
                              average=settings.get_ndarry(average_datas),
                              maximum=settings.get_ndarry(maximum_datas),
                              title='E盘' + name, subtitle=True, unit=unit)()
                graphs.append({'E盘': graph})

            if disk_home_data:
                minimum.append({'/home盘': round(self.min(disk_home_data) / rate, 2)})
                average.append({'/home盘': round(self.aver(disk_home_data) / rate, 2)})
                maximum.append({'/home盘': round(self.max(disk_home_data) / rate, 2)})
                maxtimes.append({'/home盘': len(self.maxtime(disk_home_data))})

                minimum_datas, average_datas, maximum_datas = self.deal_with_timestamp(disk_home_data, rate)
                graph = Graph(minimum=settings.get_ndarry(minimum_datas),
                              average=settings.get_ndarry(average_datas),
                              maximum=settings.get_ndarry(maximum_datas),
                              title='/home盘' + name, subtitle=True, unit=unit)()
                graphs.append({'/home盘': graph})
        else:
            minimum = round(self.min(datas) / rate, 2)
            average = round(self.aver(datas) / rate, 2)
            maximum = round(self.max(datas) / rate, 2)
            maxtimes = len(self.maxtime(datas))

            minimum_datas, average_datas, maximum_datas = self.deal_with_timestamp(datas, rate)
            graph = Graph(minimum=settings.get_ndarry(minimum_datas),
                          average=settings.get_ndarry(average_datas),
                          maximum=settings.get_ndarry(maximum_datas),
                          title=name, subtitle=True, unit=unit)
            graphs = graph()
        return minimum, average, maximum, maxtimes, graphs


def query_server_data(Dimensions=None):
    metrics = [
        # CPU
        settings.AliyunMetrics.cpu_total,

        # 内存
        settings.AliyunMetrics.memory_totalspace,
        settings.AliyunMetrics.memory_usedutilization,
        settings.AliyunMetrics.memory_actualusedspace,

        # 磁盘
        # settings.AliyunMetrics.diskusage_total,
        settings.AliyunMetrics.disk_readbytes,
        settings.AliyunMetrics.disk_writebytes,
        settings.AliyunMetrics.disk_readiops,
        settings.AliyunMetrics.disk_writeiops,

        # 带宽
        settings.AliyunMetrics.VPC_PublicIP_InternetInRate,
        settings.AliyunMetrics.VPC_PublicIP_InternetOutRate,
        settings.AliyunMetrics.net_tcpconnection,
    ]

    if not Dimensions:
        return None
    api = AliyunApi(Dimensions=Dimensions)
    for metric in metrics:
        # metric,(minimum, average, maximum, maxtimes)
        name = metric.get('name')
        yield name, api.deal_with_query(name=name,
                                        metric=metric.get('metric'),
                                        rate=metric.get('rate', 1),
                                        unit=metric.get('unit', None))


if __name__ == '__main__':
    # api = AliyunApi(Dimensions=settings.AliyunHosts[0].get('Dimensions', None))
    datas = query_server_data(Dimensions=settings.AliyunHosts[0].get('Dimensions', None))
    for data in datas:
        pass
    # data = api.query(settings.AliyunMetrics.disk_readbytes.get('metric'))
    # print(json.dumps(data, indent=2))
