import numpy as np
import time, importlib, calendar, os

from datetime import datetime, timedelta
from config import aliyun_settings, zabbix_settings


class GlobalSettings(object):
    def __init__(self):
        self.Period = 15 * 60
        self.curTime = time.time()
        self.Length = 7 * 24 * 60 * 60
        self.object_settings = ['AliyunMetrics']
        # 计算一个月有多少天
        self.mdays = calendar.mdays[time.localtime(self.curTime).tm_mon]
        self.TimeFormat = '%Y-%m-%d 00:00:00'
        self.StartTime = self.strftime(self.curTime - self.Length, self.TimeFormat)
        self.EndTime = self.strftime(self.curTime, self.TimeFormat)
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.extend()

    def extend(self):

        for key in dir(aliyun_settings):
            value = getattr(aliyun_settings, key)
            if not key.startswith('__'):
                setattr(self, key, value)

        for key in dir(zabbix_settings):
            value = getattr(zabbix_settings, key)
            # if isinstance(value, (str, list, tuple, dict)):
            if not key.startswith('__'):
                setattr(self, key, value)

    def strftime(self, ftime, format='%Y-%m-%d %H:%M:%S'):
        return time.strftime(format, time.localtime(ftime))

    def strptime(self, stime, format='%Y-%m-%d %H:%M:%S'):
        timeArray = time.strptime(stime, format)
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    def numpytime(self, dtime):
        return np.datetime64(datetime.fromtimestamp(dtime))

    def get_ndarry(self, datas, accuracy=30):
        # 24*60*60/30 = 2880条/天，120条/小时
        if len(datas) > 1000:
            return np.array(datas[::accuracy], dtype=[('date', '<M8[ns]'), ('datas', 'float64')]).view(np.recarray)
        return np.array(datas, dtype=[('date', '<M8[ns]'), ('datas', 'float64')]).view(np.recarray)


settings = GlobalSettings()
