#!/usr/bin/python
# coding: utf-8
# describe：CMDB采集脚本，对python版本和执行用户没要求
# 解决python执行编码问题
import sys

try:
    reload(sys)  # py3没有
    sys.setdefaultencoding('utf8')
except:
    pass

import socket, fcntl, struct
from datetime import datetime, date, timedelta
import os, json

try:
    from urllib import request
except:
    import urllib2 as request
import logging

# 当前目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 日志配置
log_file = os.path.join(BASE_DIR, "collect.log")
logging.basicConfig(level=logging.INFO, filename=log_file, format="%(asctime)s - [%(levelname)s] %(message)s")


def get_ip_address(nic):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', nic[:15]))[20:24])


class GetData:
    def __init__(self):
        self.result = {}

    # 解析文件
    def parse_file(self, file, name):
        with open(file) as f:
            for line in f.readlines():
                key, value = line.split(":")
                key = key.strip()
                value = value.strip()
                if key == name:
                    return value

    # 获取主机名
    def hostname(self):
        hostname = socket.gethostname()
        hostname_backup = '/tmp/.hostname'
        if os.path.isfile(hostname_backup) and os.path.getsize(hostname_backup) != 0:
            with open(hostname_backup) as f:
                hostname = f.read().strip()
        else:
            with open(hostname_backup, 'w') as f:
                f.write(hostname)
        return hostname

    # 识别主机状态
    def machine_type(self):
        result = os.popen("dmesg |grep -i virtual |grep -ci hardware")
        if int(result.read()) >= 1:
            type = "physical_machine"  # 物理机
        else:
            result = os.popen("dmesg |grep -i virtual |grep -ci kvm")
            if int(result.read()) >= 1:
                type = "cloud_vm"  # 云主机
            else:
                type = "vm"  # 虚拟机
        return type

    # 获取系统版本，兼容centos7和Ubuntu
    def os_version(self):
        with open("/etc/issue") as f:
            if f.readline().strip() == "\S":
                with open("/etc/redhat-release") as f1:
                    os_version = f1.readline().strip()
                    return os_version
            else:
                version = "no_CentOS"
                # 不知道什么原因UBuntu直接返回系统版本为空
        if version == "no_CentOS":
            with open('/etc/issue') as f:
                os_version = f.readline().strip()
                return os_version

    # 系统启动时间
    def system_up_time(self):
        with open("/proc/uptime") as f:
            s = f.read().split(".")[0]  # 启动有多少秒
        up_time = datetime.now() - timedelta(seconds=float(s))  # 当前时间减去启动秒
        return date.strftime(up_time, '%Y-%m-%d')

    def public_ip(self):
        private_ip = self.private_ip()
        ip_api_url = ['http://ip.renfei.net', 'http://ifconfig.me/ip']
        ip_list = []
        try:
            req = request.Request(url=ip_api_url[0])
            res = request.urlopen(req)
            ip = json.loads(res.read().decode())['clientIP']
        except:
            req = request.Request(url=ip_api_url[1])
            res = request.urlopen(req)
            ip = res.read().decode()
        if ip in private_ip:
            ip.append(ip)
            return ip_list
        else:
            ip_list.append('%s(NAT)' % ip)
            return ip_list

    def private_ip(self):
        nic_prefix = ['eth', 'en', 'em']  # 常见网卡名前缀
        ip_list = []
        with open("/proc/net/dev") as f:
            for s in f.readlines():
                name = s.split(':')[0].strip()
                for p in nic_prefix:
                    if name.startswith(p):
                        result = os.popen("ip addr show %s |awk -F'[ /]' '/inet /{print $6}'" % name)
                        ip_list.append(result.read().strip())
        # 删除有网卡但是没有具体ip的空字符串
        for ip in ip_list:
            if len(ip) == 0:
                ip_list.remove(ip)
        return ip_list

    def cpu_num(self):
        cpu = self.parse_file("/proc/cpuinfo", "cpu cores")
        return "%s Core" % cpu

    def cpu_model(self):
        model = self.parse_file("/proc/cpuinfo", "model name")
        return model

    def memory(self):
        total = self.parse_file("/proc/meminfo", "MemTotal")
        total = round(float(total.split()[0]) / 1024 / 1024, 1)  # 转GB单位
        return "%sG" % total

    def disk(self):
        disk = []
        result = os.popen("lsblk |awk '$6~/disk/{print $1,$4,$5}'")
        for d in result.read().strip().split('\n'):
            d = d.split()
            device = d[0]
            size = d[1]
            type = "HDD" if d[2] == 0 else "SSD"
            disk.append({'device': '/dev/%s' % device, 'size': size, 'type': type})
        return disk

    def get_all(self):
        """
        这里字段必须与API对应
        """
        self.result = {
            "hostname": self.hostname(),
            "machine_type": self.machine_type(),
            "os_version": self.os_version(),
            "public_ip": self.public_ip(),
            "private_ip": self.private_ip(),
            "cpu_num": self.cpu_num(),
            "cpu_model": self.cpu_model(),
            "memory": self.memory(),
            "disk": self.disk(),
            "put_shelves_date": self.system_up_time(),  # 上架时间默认设置系统启动时间
        }
        # json_data = json.dumps(self.result)
        return self.result


def main():
    data = GetData()
    try:
        result = {'code': 200, 'msg': '采集脚本执行成功！', "data": data.get_all()}
        print(json.dumps(result))
    except Exception as e:
        result = {'code': 500, 'msg': '采集脚本执行失败！错误：%s' % e}
        print(json.dumps(result))


main()
