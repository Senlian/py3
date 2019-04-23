# 服务器性能分析报告生成工具 #

## 基础配置 ##
- aliyun_metric
    > 阿里云监控项配置
    
- aliyun_settings
    > aliyun api设置，账号密码，区域，工程名等
    
- zabbix_settings
    > zabbix api设置，监控项，api，用户名密码等

- settings
    > 设置汇总，统一调用接口
    
            
## 阿里云数据导出 ##
```aliyun-python-sdk
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.request import CommonRequest
    from aliyunsdkcms.request.v20180308 import QueryMetricListRequest
```

## Zabbix数据导出 ##
[zabbix api文档](<http://www.zabbix.com/documentation/3.4/zh/manual/api/reference/host/get>)


## 图表绘制 ##
[matplotlib官方文档](<https://matplotlib.org/api/_as_gen/matplotlib.pyplot.html#module-matplotlib.pyplot>)

[matplotlib中文文档](<https://www.matplotlib.org.cn/gallery/text_labels_and_annotations/figlegend_demo.html>)

## 模板渲染 ##
- 模板数据
    - 日期
        date = {'stime':stime, 'etime':etime}
    - 服务器列表
        hosts =[{'name':name,'host':host}]
    - 监控数据表
        tables = [{
            'host': 'host',
            'metrics': [{
                    'name': 'name',
                    'minimum': '',
                    'average': '',
                    'maximum': '',
                    'peak_times': ''
            }]}]
    - 图片
        graphs = [{
            'host': 'host',
            'graphs': []
        }]
        
## 主程序 ##
