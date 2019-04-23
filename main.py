#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, time
from zabbix.zabbix_api import ZabbixApi, query_host_data
from aliyun.aliyun_api import AliyunApi, query_server_data
from config.settings import settings
from report.report import Report


def main():
    report = Report(docName='金棋牌性能监控报告{0}'.format(time.strftime("%Y-%m-%d")))
    zabbix = ZabbixApi()
    zabbix_hosts = zabbix.host_list()

    # 添加了zabbix监控的阿里云服务器
    for server in settings.AliyunHosts:
        report.add_host(name=server.get('name'), ip=server.get('host'))

        metric_box = []
        graph_box = []
        host = server.get('host', None)
        Dimensions = server.get('Dimensions', None)
        aliyun_datas = query_server_data(Dimensions=Dimensions)
        print(server.get('name'))
        # name, (minimum, average, maximum, maxtimes, graphs)
        if aliyun_datas:
            for name, datas in aliyun_datas:
                if not datas or not name:
                    continue
                print(name)
                (minimum, average, maximum, maxtimes, graphs) = datas
                if isinstance(minimum, list):
                    for sub_min, sub_aver, sub_max, sub_times, sub_graphs in (
                            zip(minimum, average, maximum, maxtimes, graphs)):
                        device = (list(sub_min.keys())[0])
                        metric_box.append({
                            'name': device + name,
                            'minimum': sub_min[device],
                            'average': sub_aver[device],
                            'maximum': sub_max[device],
                            'maxtimes': sub_times[device]
                        })
                        graph_box.append(sub_graphs[device])
                else:
                    metric_box.append({
                        'name': name,
                        'minimum': minimum,
                        'average': average,
                        'maximum': maximum,
                        'maxtimes': maxtimes
                    })
                    graph_box.append(graphs)

        if (server.get('host') in [host.get('host') for host in zabbix_hosts]):
            zabbix_datas = query_host_data(host=host)
            # name, (minimum, average, maximum, maxtimes, graphs)
            if zabbix_datas:
                for name, datas in zabbix_datas:
                    if not datas or not name:
                        continue
                    print(name)
                    (minimum, average, maximum, maxtimes, graphs) = datas
                    metric_box.append({
                        'name': name,
                        'minimum': minimum,
                        'average': average,
                        'maximum': maximum,
                        'maxtimes': maxtimes
                    })
                    graph_box.append(graphs)

        if metric_box:
            report.add_table({'host': server.get('name'), 'metrics': metric_box})
        if graph_box:
            report.add_graph({'host': server.get('name'), 'graphs': graph_box})
    report.save()


if __name__ == '__main__':
    main()
