#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: ECS基础监控项,set_Metric
class Ecs_Base_Metric():
    # CPU百分比,%
    CPUUtilization = {'name': 'CPU百分比(%)', 'metric': 'CPUUtilization', 'unit': '%%', 'rate': 1}
    # 公网流入带宽,bits/s
    InternetInRate = {'name': '公网流入带宽(bytes/s)', 'metric': 'InternetInRate', 'unit': 'bytes/s', 'rate': 8}
    # 公网流出带宽,bits/s
    InternetOutRate = {'name': '公网流出带宽(bytes/s)', 'metric': 'InternetOutRate', 'unit': 'bytes/s', 'rate': 8}

    # 公网流出带宽使用率,%
    InternetOutRate_Percent = {'name': '公网流出带宽使用率(%)', 'metric': 'InternetOutRate_Percent', 'unit': '%%', 'rate': 1}

    # 私网流入带宽,bits/s
    IntranetInRate = {'name': '私网流入带宽(bytes/s', 'metric': 'IntranetInRate', 'unit': 'bytes/s', 'rate': 8}

    # 私网流出带宽,bits/s
    IntranetOutRate = {'name': '私网流出带宽(bytes/s)', 'metric': 'IntranetOutRate', 'unit': 'bytes/s', 'rate': 8}

    # 系统磁盘总读BPS,Bps
    DiskReadBPS = {'name': '系统磁盘总读BPS(MBps)', 'metric': 'DiskReadBPS', 'unit': 'MBps', 'rate': 1024}

    # 系统磁盘总写BPS,Bps
    DiskWriteBPS = {'name': '系统磁盘总写BPS(MBps)', 'metric': 'DiskWriteBPS', 'unit': 'MBps', 'rate': 1024}

    # 系统磁盘读IOPS,Count/Second
    DiskReadIOPS = {'name': '系统磁盘读IOPS(count/s)', 'metric': 'DiskReadIOPS', 'unit': 'Times/s', 'rate': 1}

    # 系统磁盘写IOPS,Count/Second
    DiskWriteIOPS = {'name': '系统磁盘写IOPS(count/s)', 'metric': 'DiskWriteIOPS', 'unit': 'Times/s', 'rate': 1}

    # 专有网络公网流入带宽,bits/s
    VPC_PublicIP_InternetInRate = {'name': '专有网络公网流入带宽(bytes/s)', 'metric': 'VPC_PublicIP_InternetInRate',
                                   'unit': 'bytes/s', 'rate': 8}

    # 专有网络公网流出带宽,bits/s
    VPC_PublicIP_InternetOutRate = {'name': '专有网络公网流出带宽(bytes/s)', 'metric': 'VPC_PublicIP_InternetOutRate',
                                    'unit': 'bytes/s', 'rate': 8}

    # 专有网络公网流出带宽使用率,%
    VPC_PublicIP_InternetOutRate_Percent = {'name': '专有网络公网流出带宽使用率(%)',
                                            'metric': 'VPC_PublicIP_InternetOutRate_Percent', 'unit': '%%', 'rate': 1}


# TODO: ECS系统监控项,set_Metric
class Ecs_Sys_Metric():
    # TODO: CPU
    # Host.cpu.idle，当前空闲CPU百分比,%
    cpu_idle = {'name': '当前空闲CPU百分比(%)', 'metric': 'cpu_idle', 'unit': '%%', 'rate': 1}

    # Host.cpu.system，当前内核空间占用CPU百分比,%
    cpu_system = {'name': '当前内核空间占用CPU百分比(%)', 'metric': 'cpu_system', 'unit': '%%', 'rate': 1}

    # Host.cpu.user，当前用户空间占用CPU百分比,%
    cpu_user = {'name': '当前用户空间占用CPU百分比(%)', 'metric': 'cpu_user', 'unit': '%%', 'rate': 1}

    # Host.cpu.iowait，当前等待IO操作的CPU百分比,%
    cpu_wait = {'name': '当前等待IO操作的CPU百分比(%)', 'metric': 'cpu_wait', 'unit': '%%', 'rate': 1}

    # Host.cpu.other，其他占用CUP百分比，其他消耗，计算方式为（Nice + SoftIrq + Irq + Stolen）的消耗,%
    cpu_other = {'name': '其他占用CUP百分比(%)', 'metric': 'cpu_other', 'unit': '%%', 'rate': 1}

    # Host.cpu.total，当前消耗的总CPU百分比,%
    cpu_total = {'name': '当前消耗的总CPU百分比(%)', 'metric': 'cpu_total', 'unit': '%%', 'rate': 1}

    # TODO: 内存
    # Host.mem.total，内存总量,bytes
    memory_totalspace = {'name': '内存总量(GB)', 'metric': 'memory_totalspace', 'unit': 'GB', 'rate': 1024 * 1024 * 1024}

    # Host.mem.used，已用内存量 ，用户程序使用的内存 + buffers + cached，buffers为缓冲区占用的内存空间，cached为系统缓存占用的内存空间,bytes
    memory_usedspace = {'name': '已用内存量(GB)', 'metric': 'memory_usedspace', 'unit': 'GB', 'rate': 1024 * 1024 * 1024}

    # Host.mem.actualused，用户实际使用的内存，计算方法为（used - buffers - cached）,bytes
    memory_actualusedspace = {'name': '用户实际使用的内存(GB)', 'metric': 'memory_actualusedspace', 'unit': 'GB',
                              'rate': 1024 * 1024 * 1024}

    # Host.mem.free，剩余内存量,bytes
    memory_freespace = {'name': '剩余内存量(GB)', 'metric': 'memory_freespace', 'unit': 'GB', 'rate': 1024 * 1024 * 1024}

    # Host.mem.freeutilization， 剩余内存百分比,%
    memory_freeutilization = {'name': '剩余内存百分比(%)', 'metric': 'memory_freeutilization', 'unit': '%%', 'rate': 1}

    # Host.mem.usedutilization，内存使用率,%
    memory_usedutilization = {'name': '内存使用率(%)', 'metric': 'memory_usedutilization', 'unit': '%%', 'rate': 1}

    # TODO: 磁盘
    # Host.diskusage.used，磁盘的已用存储空间,bytes
    diskusage_used = {'name': '磁盘的已用存储空间(GB)', 'metric': 'diskusage_used', 'unit': 'GB', 'rate': 1024 * 1024 * 1024}

    # Host.disk.utilization，磁盘使用率,%
    diskusage_utilization = {'name': '磁盘使用率(%)', 'metric': 'diskusage_utilization', 'unit': '%%', 'rate': 1}

    # Host.diskusage.free，磁盘的剩余存储空间,bytes
    diskusage_free = {'name': '磁盘的剩余存储空间(GB)', 'metric': 'diskusage_free', 'unit': 'GB', 'rate': 1024 * 1024 * 1024}

    # Host.diskussage.total，磁盘存储总量,bytes
    diskusage_total = {'name': '磁盘存储总量(GB)', 'metric': 'diskusage_total', 'unit': 'GB', 'rate': 1024 * 1024 * 1024}

    # Host.disk.readbytes，磁盘每秒读取的字节数,bytes/s
    disk_readbytes = {'name': '磁盘每秒读取的字节数(M/s)', 'metric': 'disk_readbytes', 'unit': 'M/s', 'rate': 1024 * 1024}

    # Host.disk.writebytes，磁盘每秒写入的字节数,bytes/s
    disk_writebytes = {'name': '磁盘每秒写入的字节数(M/s)', 'metric': 'disk_writebytes', 'unit': 'M/s', 'rate': 1024 * 1024}

    # Host.disk.readiops，磁盘每秒的读请求数量,次/秒
    disk_readiops = {'name': '磁盘每秒的读请求数量(次/秒)', 'metric': 'disk_readiops', 'unit': 'Times/s', 'rate': 1}

    # Host.disk.writeiops，磁盘每秒的写请求数量,次/秒
    disk_writeiops = {'name': '磁盘每秒的写请求数量(次/秒)', 'metric': 'disk_writeiops', 'unit': 'Times/s', 'rate': 1}

    # TODO: FS,%
    fs_inodeutilization = {'name': 'FS(%)', 'metric': 'fs_inodeutilization', 'unit': '%%', 'rate': 1}

    # TODO: 网卡
    # Host.netin.rate，网卡每秒接收的比特数，即网卡的上行带宽,bits/s
    networkin_rate = {'name': '网卡的上行带宽(bytes/s)', 'metric': 'networkin_rate', 'unit': 'bytes/s', 'rate': 8}

    # Host.netout.rate，网卡每秒发送的比特数，即网卡的下行带宽,bits/s
    networkout_rate = {'name': '网卡的下行带宽(bytes/s)', 'metric': 'networkout_rate', 'unit': 'bytes/s', 'rate': 8}

    # Host.netin.packages，网卡每秒接收的数据包数,个/秒
    networkin_packages = {'name': '网卡每秒接收的数据包数(个/秒)', 'metric': 'networkin_packages', 'unit': 'num/s', 'rate': 1}

    # Host.netout.packages，网卡每秒发送的数据包数,个/秒
    networkout_packages = {'name': '网卡每秒发送的数据包数(个/秒)', 'metric': 'networkout_packages', 'unit': 'num/s', 'rate': 1}

    # Host.netin.errorpackage，设备驱动器检测到的接收错误包的数量,个/秒
    networkin_errorpackages = {'name': '设备驱动器检测到的接收错误包的数量(个/秒)', 'metric': 'networkin_errorpackages', 'unit': 'num/s',
                               'rate': 1}

    # Host.netout.errorpackages，设备驱动器检测到的发送错误包的数量,个/秒
    networkout_errorpackages = {'name': '设备驱动器检测到的发送错误包的数量(个/秒)', 'metric': 'networkout_errorpackages', 'unit': 'num/s',
                                'rate': 1}

    # TODO: TCP连接数
    # Host.tcpconnection，各种状态下的TCP连接数包括LISTEN、SYN_SENT、ESTABLISHED、SYN_RECV、FIN_WAIT1、CLOSE_WAIT、FIN_WAIT2、LAST_ACK、TIME_WAIT、CLOSING、CLOSED,个
    net_tcpconnection = {'name': 'TCP连接数(个)', 'metric': 'net_tcpconnection', 'unit': None, 'rate': 1}


class AliyunMetrics(object):
    def __init__(self):
        self.base = Ecs_Base_Metric()
        self.sys = Ecs_Sys_Metric()

        for key in dir(self.base):
            value = getattr(self.base, key)
            if not key.startswith('__'):
                setattr(self, key, value)

        for key in dir(self.sys):
            value = getattr(self.sys, key)
            if not key.startswith('__'):
                setattr(self, key, value)


a = AliyunMetrics()
