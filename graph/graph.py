#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import json, random, string, os, base64

from io import StringIO, BytesIO
from datetime import datetime, timedelta
from matplotlib.font_manager import FontManager

from config.settings import settings


class Graph(object):
    def __init__(self, minimum=None, average=None, maximum=None, unit=None,
                 title=None, subtitle=False, xlabel=None, ylabel=None, outdir='output/imgs'):
        if (minimum is None) and (average is None) and (maximum is None):
            return None
        self.outdir = outdir
        self.fig = plt.figure(num=1, facecolor='#000000')
        # 调整子图间距
        # self.fig.subplots_adjust(top=100)
        self.title = title
        if title:
            self.fig.suptitle(title, fontsize=20, fontweight='bold', fontdict={'color': 'w', 'family': 'SimHei'})
        # 添加子图，111表示子图数量及位置
        # facecolor背景色，edgecolor边框颜色
        # self.ax = self.fig.add_subplot(111, facecolor='#000000')

        # 获取主图坐标信息
        self.ax = self.fig.gca(facecolor='#000000')

        # 设置子图位置， left, bottom, x拉伸,y拉伸
        l, b, w, h = self.ax.get_position().bounds
        # self.ax.set_position(pos=(l, b, w, h + 0.08))
        self.ax.set_position(pos=(l, b - 0.01, w, h + 0.1))

        # 添加栅格，透明度0.15, 1表示完全不透明
        self.ax.grid(alpha=0.15)

        # 日期坐标轴的显示格式，要求必须有numpy日期格式数据，否则报错
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))

        # 坐标轴刻度及文字格式控制,pad设置刻度间距
        self.ax.tick_params(axis='both', color='gray', labelcolor='w', pad=10, labelsize=7)

        # 坐标边框颜色
        self.ax.spines['left'].set_color('gray')
        self.ax.spines['bottom'].set_color('gray')
        # x轴，y轴的数据偏移量
        self.ax.margins(x=0, y=0)

        # 自动调整X轴刻度样式，避免重叠
        # self.fig.autofmt_xdate()

        if xlabel:
            # x轴标题
            self.ax.set_xlabel(xlabel, fontdict={'color': 'w', 'family': 'SimHei'})
        if ylabel:
            # y轴标题
            self.ax.set_ylabel(ylabel, fontproperties="SimHei", fontdict={'color': 'w'})
        data_min = data_aver = data_max = 0
        peak_time = None
        offset_left = 0.5
        # 添加线条
        if isinstance(minimum, np.ndarray):
            data_min = minimum.datas.min()
            data_aver = minimum.datas.mean()
            data_max = minimum.datas.max()
            peak_time = minimum.date[minimum.datas.argmax()]
            # 添加数据线
            self.ax.plot_date(minimum.date, minimum.datas, fmt='-', color='b', alpha=0.6, label='minimum')
            # 按条件阴影填充
            self.ax.fill_between(minimum.date, y1=data_min, y2=minimum.datas,
                                 where=minimum.datas >= data_min, color='b', alpha=0.2)
            # np.timedelta64(1, 'D')表示一天
            # np.datetime64(minimum.date[0], 'D')日期转换到%Y/%m/%d格式
            # 解决X轴两端时间缺失问题
            self.ax.set_xlim(np.datetime64(minimum.date[0], 'D'),
                             np.datetime64(minimum.date[-1] + np.timedelta64(1, 'D') - np.timedelta64(1, 'h'), 'D'),
                             auto=True)
            offset_left -= 0.13

        if isinstance(average, np.ndarray):
            if not isinstance(minimum, np.ndarray):
                data_min = average.datas.min()
            data_aver = average.datas.mean()
            data_max = average.datas.max()
            peak_time = average.date[average.datas.argmax()]
            # 添加数据线
            self.ax.plot_date(x=average.date, y=average.datas, fmt='-', color='#40E0D0', alpha=0.6, label='average')
            # 阴影填充
            self.ax.fill_between(average.date, y1=average.datas.min(), y2=average.datas,
                                 where=average.datas >= average.datas.min(), color='#40E0D0', alpha=0.2)
            self.ax.set_xlim(np.datetime64(average.date[0], 'D'),
                             np.datetime64(average.date[-1] + np.timedelta64(1, 'D') - np.timedelta64(1, 'h'), 'D'),
                             auto=True)
            offset_left -= 0.13

        if isinstance(maximum, np.ndarray):
            data_max = maximum.datas.max()
            peak_time = maximum.date[maximum.datas.argmax()]
            # 添加数据线
            self.ax.plot_date(maximum.date, maximum.datas, fmt='-', color='r', alpha=0.6, label='maximum')
            # 阴影填充
            self.ax.fill_between(maximum.date, y1=maximum.datas.min(), y2=maximum.datas,
                                 where=maximum.datas >= maximum.datas.min(), color='r', alpha=0.2)
            self.ax.set_xlim(np.datetime64(maximum.date[0], 'D'),
                             np.datetime64(maximum.date[-1] + np.timedelta64(1, 'D') - np.timedelta64(1, 'h'), 'D'),
                             auto=True)

            offset_left -= 0.13

        # 设置图例样式
        if offset_left < 0.3:
            self.ax.legend(framealpha=0.3, loc='center left', edgecolor='none', facecolor='w',
                           bbox_to_anchor=(offset_left, -0.18), labelspacing=5, shadow=False, ncol=3, borderaxespad=0)

        if subtitle:
            # 子图标题
            notes = 'Minimum:{0}  Average:{1}  Maximum:{2}'.format(round(data_min, 2),
                                                                   round(data_aver, 2),
                                                                   round(data_max, 2))
            if peak_time:
                notes += '  Peak_Time:{0}'.format(str(peak_time)[:-10])
            self.ax.set_title(notes, loc='center', pad=5,
                              fontdict={'color': 'lightblue', 'size': '10', 'family': 'SimHei'})

        # y轴样式控制
        if unit:
            if 0 < data_max < 10:
                self.ax.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%1.2f {0}'.format(unit)))
            else:
                self.ax.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%d {0}'.format(unit)))

        # 设置显影坐标刻度
        # [label.set_visible(False) for label in self.ax.get_xticklabels()]
        # [label.set_visible(True) for label in self.ax.get_xticklabels()[::1]]

        # 隐藏X轴
        # self.ax.xaxis.set_visible(False)
        # x轴的数据范围设置

    def show(self):
        self.fig.show()

    def binary_img(self):
        # https://blog.csdn.net/C_chuxin/article/details/84000438
        # IO流
        # buff = StringIO()
        # 二进制流
        buff = BytesIO()
        # 数据保存入流
        self.fig.savefig(buff, format='png', bbox_inches='tight', transparent=False, facecolor='#000000', dpi=100,
                         quality=80)
        # 数据打印入二进制流
        # self.fig.canvas.print_png(buff)

        buff.seek(0)
        return base64.b64encode(buff.getvalue()).decode()

    def save(self):
        filename = self.title.strip('/').strip('\\') or ''.join(
            random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits, 16))
        dirpath = os.path.join(settings.BASE_DIR, self.outdir.strip('/').strip('\\'))
        filename = os.path.join(dirpath, "{}.png".format(filename.split('(')[0]))
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        self.fig.savefig(filename, bbox_inches='tight', transparent=False, facecolor='#000000', dpi=100, quality=80)
        return filename

    def __call__(self, *args, **kwargs):
        # 显示
        self.show()
        # 保存到本地文件
        self.save()
        # 保存成bytes数据流
        return self.binary_img()


if __name__ == '__main__':
    # from zabbix.zabbix_api import ZabbixApi
    #
    # api = ZabbixApi()
    #
    # datas = api.metric_data('29968', 3) or api.metric_data('29968', 0)
    #
    # datas = (api.get_values_with_stamp(datas))
    # 'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'
    # #556B2F #006400
    # t = datas[0][0]
    # print(np.datetime64(datetime.fromtimestamp(t)))
    # print(len(datas))
    # 24*60*60/30 = 2880条/天，120条/小时
    # np_datas = np.array(datas[::30], dtype=[('date', '<M8[ns]'), ('datas', 'float64')]).view(np.recarray)

    g = Graph(minimum=np_datas, title='CPU使用率(%)', note=True, unit='%%')
    print(g.show())
