import traceback
import paramiko
from io import StringIO  # py2 from StringIO import StringIO
import logging
import socket
from paramiko import ssh_exception
from paramiko.ssh_exception import AuthenticationException


class SSH:
    def __init__(self, ip, port, username, password=None, key=None):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.key = key

    def command(self, shell):
        # 绑定实例
        ssh_client = paramiko.SSHClient()
        ssh = ssh_client
        # 允许连接不在known_hosts文件上的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.password:
            ssh.connect(hostname=self.ip, port=self.port, username=self.username, password=self.password, timeout=5)
        else:
            cache = StringIO(self.key)  # 将字符串通过StringIO转为file对象（self.key内容是从数据库查询的文本）
            key = paramiko.RSAKey.from_private_key(cache)  # 接收file对象
            # 使用key登录
            ssh.connect(hostname=self.ip, port=self.port, username=self.username, pkey=key)

        # 执行Shell命令，结果分别保存在标准输入，标准输出和标准错误
        stdin, stdout, stderr = ssh.exec_command(shell)
        stdout = stdout.read()
        error = stderr.read()
        # 判断stderr输出是否为空，为空则打印运行结果，不为空打印报错信息
        ssh.close()
        if not error:
            return stdout.decode('utf-8')
        else:
            return error.decode("utf-8")

    def scp(self, local_file, remote_file):
        # 绑定实例
        ts = paramiko.Transport(self.ip, self.port)
        try:
            if self.password:
                ts.connect(username=self.username, password=self.password)
            else:
                cache = StringIO(self.key)
                key = paramiko.RSAKey.from_private_key(cache)
                ts.connect(username=self.username, pkey=key)
            sftp = paramiko.SFTPClient.from_transport(ts)
            try:
                sftp.put(localpath=local_file, remotepath=remote_file)
                ts.close()
                return "上传文件成功"
            except Exception as e:
                return "上传文件失败：%s" % e
        except Exception as e:
            return "SSH连接失败：%s" % e

    def test(self):
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            conn.connect(hostname=self.ip, port=self.port, username=self.username, password=self.password, timeout=5)
            connect_result = "Connect Server {0} {1} {2} 主机连接成功!\n".format(
                self.ip, self.port, self.port,)
            # 记录连接成功日志
            logging.info(connect_result)
            data = {"code": 200, "msg": "主机连接成功"}
        except AuthenticationException:
            connect_result = "Connect Server {0} {1} {2} 用户名或密码错误!\n".format(
                self.ip, self.port, self.username, )
            # 用户名或密码错误
            print(traceback.format_exc())
            logging.info(connect_result)
            data = {"code": 403, "msg": "用户名或密码错误"}
        except socket.timeout:
            connect_result = "Connect Server {0} {1} {2} 主机连接异常!\n".format(
                self.ip, self.port, self.username)
            # 主机连接异常
            print(traceback.format_exc())
            logging.info(connect_result)
            data = {"code": 600, "msg": "主机连接异常 检查一下主机信息是否更改"}
        except ssh_exception.NoValidConnectionsError:
            connect_result = "Connect Server {0} {1} {2} 端口错误!\n".format(
                self.ip, self.port, self.username)
            # 端口错误
            print(traceback.format_exc())
            logging.info(connect_result)  # 输出错误信息日志
            data = {"code": 700, "msg": "端口错误"}
        return data
