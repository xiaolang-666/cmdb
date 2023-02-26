import json
import os
import time
from json.decoder import JSONDecodeError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from cmdb.models import Idc, ServerGroup, Server, IiotDocument
from cmdb.serializers import IdcSerializer, ServerGroupSerializer, ServerSerializer, IiotDocumentSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from devops_api import settings
from system_config.models import Credential
from cmdb.utils.ssh import SSH
from django.http import FileResponse
from rest_framework.permissions import IsAuthenticated
from libs.aliyun_cloud import AliCloud


class IdcViewSet(ModelViewSet):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]  # 指定过滤器
    search_fields = ('name',)  # 指定可搜索的字段
    filterset_fields = ['city']  # 指定过滤的字段

    def create(self, request, *args, **kwargs):
        idc = Idc.objects.filter(name=request.data.get('name'))
        city = Idc.objects.filter(name=request.data.get('city'))
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
            res = {'code': 500, 'msg': '该机房和城市已存在！'}
            return Response(res)
        self.perform_create(serializer)
        res = {'code': 200, 'msg': '创建成功'}
        return Response(res)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        result = {'code': 200, 'msg': 'idc信息更新成功！'}

        return Response(result)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except Exception as e:
            print(e)
            result = {"code": 500, "msg": "该IDC机房关联了其他主机，请先删除其关联的对象！"}
            return Response(result)
        result = {"code": 200, "msg": "删除IDC机房成功！"}
        return Response(result)

    def perform_destroy(self, instance):
        instance.delete()


class ServerGroupViewSet(ModelViewSet):
    queryset = ServerGroup.objects.all()
    serializer_class = ServerGroupSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]  # 指定过滤器
    search_fields = ('name',)  # 指定可搜索的字段

    def create(self, request, *args, **kwargs):
        server_group = ServerGroup.objects.filter(name=request.data.get('name'))
        if not server_group:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            res = {'code': 200, 'msg': '创建成功'}
        else:
            res = {'code': 500, 'msg': '该分组已存在！'}
        return Response(res)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        result = {'code': 200, 'msg': '主机组信息更新成功！'}

        return Response(result)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except Exception as e:
            print(e)
            result = {"code": 500, "msg": "该分组关联了其他主机，请先删除其关联的对象！"}
            return Response(result)
        result = {"code": 200, "msg": "删除分组成功！"}
        return Response(result)

    def perform_destroy(self, instance):
        instance.delete()


class ServerViewSet(ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]  # 指定过滤器
    search_fields = ('name',)  # 指定可搜索的字段

    def create(self, request, *args, **kwargs):
        server_group = ServerGroup.objects.filter(name=request.data.get('name'))
        if not server_group:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            res = {'code': 200, 'msg': '创建成功'}
        else:
            res = {'code': 500, 'msg': '该主机已存在！'}
        return Response(res)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        result = {'code': 200, 'msg': '主机信息更新成功！'}

        return Response(result)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        result = {"code": 200, "msg": "删除主机成功！"}
        return Response(result)

    def perform_destroy(self, instance):
        instance.delete()


class IiotOpsDocumentView(ModelViewSet):
    queryset = IiotDocument.objects.all()
    serializer_class = IiotDocumentSerializer
    # filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]  # 指定过滤器
    search_fields = ('name',)  # 指定可搜索的字段

    def create(self, request, *args, **kwargs):
        iiot_document = IiotDocument.objects.filter(name=request.data.get('name'))
        if not iiot_document:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            res = {'code': 200, 'msg': '文档创建成功'}
        else:
            res = {'code': 500, 'msg': '该文档已存在！'}
        return Response(res)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        res = {"code": 200, "msg": "获取文档数据成功", "data": serializer.data}
        return Response(res)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        result = {'code': 200, 'msg': '文档保存成功！'}

        return Response(result)


class HostCollectView(APIView):
    """"
    主机同步数据接口
    """

    def get(self, request):
        hostname = request.query_params.get("hostname")
        server = Server.objects.filter(hostname=hostname).first()
        ssh_ip = server.ssh_ip
        ssh_port = server.ssh_port
        credential_obj = server.credential_id
        # 如果是excel导入的主机信息 默认是没有选择凭据的 防止前端报错找不到具体原因
        try:
            credential = Credential.objects.get(id=credential_obj.id)
            username = credential.username
        except Exception as e:
            result = {"code": 500, "msg": "在编辑里面指定凭据在同步数据"}
            print("同步异常：%s" % e)
            return Response(result)

        if credential.auth_mode == 1:
            password = credential.password
            ssh = SSH(ssh_ip, ssh_port, username, password=password)
        else:
            private_key = credential.private_key  # key的内容，并不是一个文件
            ssh = SSH(ssh_ip, ssh_port, username, key=private_key)

        test = ssh.test()  # 测试SSH连接通过
        if test['code'] == 200:
            client_agent_name = "host_collect.py"
            local_file = os.path.join(settings.BASE_DIR, 'cmdb', 'files', client_agent_name)
            remote_file = os.path.join(settings.CLIENT_COLLECT_DIR, client_agent_name)  # 这个工作路径在setting里配置
            ssh.scp(local_file, remote_file=remote_file)
            ssh.command('chmod +x %s' % remote_file)
            try:
                result = ssh.command('python %s' % remote_file)  # 有的主机可能没有python命令 但是有python3
                result = json.loads(result)  # 如果主机没有正常解析json格式数据的话说明python没有执行
            except JSONDecodeError:
                result = ssh.command('python3 %s' % remote_file)
                result = json.loads(result)
            if result['code'] == 200:  # 采集脚本执行成功
                data = result["data"]
                # 2.主机配置入库（自动采集）ssh验证通过
                Server.objects.filter(hostname=hostname).update(**data, is_verified="verified")
                result = {'code': 200, 'msg': '主机信息同步成功！'}
            else:
                result = {'code': 500, 'msg': '采集主机配置失败！错误：%s' % result['msg']}
        else:
            result = test
            # 后续如果更改了主机的关键信息 然后导致同步失败 则把ssh验证信息修改为unverified
            Server.objects.filter(hostname=hostname).update(is_verified="unverified")
        return Response(result)


class CreateHostView(APIView):
    def post(self, request):
        idc_id = int(request.data.get('idc'))  # 机房id
        server_group_id_list = request.data.get('server_group')  # 分组id
        name = request.data.get('name')
        ssh_ip = request.data.get('ssh_ip')
        ssh_port = int(request.data.get('ssh_port'))
        credential_id = int(request.data.get('credential_id'))
        note = request.data.get('note')

        # 通过凭据ID获取服务器用户名信息
        credential = Credential.objects.get(id=credential_id)
        username = credential.username
        if credential.auth_mode == 1:
            password = credential.password
            ssh = SSH(ssh_ip, ssh_port, username, password=password)
        else:
            private_key = credential.private_key
            ssh = SSH(ssh_ip, ssh_port, username, key=private_key)

        test = ssh.test()  # 测试SSH连接通过
        if test['code'] == 200:
            client_agent_name = "host_collect.py"
            local_file = os.path.join(settings.BASE_DIR, 'cmdb', 'files', client_agent_name)
            remote_file = os.path.join(settings.CLIENT_COLLECT_DIR, client_agent_name)  # 这个工作路径在setting里配置
            ssh.scp(local_file, remote_file=remote_file)
            ssh.command('chmod +x %s' % remote_file)
            result = ssh.command('python %s' % remote_file)  # 支持python2 和 python3 执行采集脚本
            result = json.loads(result)
            if result['code'] == 200:  # 采集脚本执行成功
                data = result["data"]
                hostname = result["data"]["hostname"]
                # 如果服务器主机存在则直接返回数据
                server = Server.objects.filter(hostname=hostname)
                if server:
                    result = {'code': 500, 'msg': '主机已存在！'}
                    return Response(result)
                # 1.基本主机信息入库（人工录入 前端传过来的数据）
                idc = Idc.objects.get(id=idc_id)  # 根据id查询IDC
                server_obj = Server.objects.create(
                    idc=idc,
                    name=name if name else hostname,
                    hostname=hostname,
                    ssh_ip=ssh_ip,
                    ssh_port=ssh_port,
                    is_verified='verified',
                    credential_id=credential,
                    note=note
                )
                # 添加对对多字段
                for group_id in server_group_id_list:
                    group = ServerGroup.objects.get(id=group_id)  # 根据id查询分组
                    server_obj.server_group.add(group)  # 将服务器添加到分组
                # 2.主机配置入库（自动采集）
                server.update(**data)
                result = {'code': 200, 'msg': '添加主机成功并同步配置完成'}
            else:
                result = {'code': 500, 'msg': '采集主机配置失败！错误：%s' % result['msg']}
        else:
            result = test
        return Response(result)


class ExcelCreateHostView(APIView):
    # 下载主机导入模板.xlsx
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        重写了get_permissions方法，
        并为GET方法返回一个空的权限列表。这将导致DRF不会对GET方法进行身份验证。
        对于所有其他HTTP方法，我们仍然使用默认的IsAuthenticated权限。
        """
        if self.request.method == 'GET':
            return []
        else:
            return super(ExcelCreateHostView, self).get_permissions()

    def get(self, request):
        file_name = 'host.xlsx'
        file_path = os.path.join(settings.BASE_DIR, 'cmdb', 'files', file_name)
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name
        return response

    # 导入excel表格
    def post(self, request):
        import xlrd
        excel_file_obj = request.data['file']
        idc_id = int(request.data.get('idc'))
        server_group_id = int(request.data.get('server_group'))
        try:
            data = xlrd.open_workbook(filename=None, file_contents=excel_file_obj.read())
        except Exception:
            result = {'code': 500, 'msg': '请上传Excel文件！'}
            return Response(result)
        table = data.sheets()[0]  # 打开第一个工作表
        nrows = table.nrows  # 获取表的行数

        idc = Idc.objects.get(id=idc_id)
        server_group = ServerGroup.objects.get(id=server_group_id)
        try:
            for i in range(nrows):  # 循环行
                if i != 0:  # 跳过标题行
                    name = table.row_values(i)[0]
                    hostname = table.row_values(i)[1]
                    ssh_ip = table.row_values(i)[2]
                    ssh_port = table.row_values(i)[3]
                    note = table.row_values(i)[4]

                    server = Server.objects.create(
                        idc=idc,
                        name=name,
                        hostname=hostname,
                        ssh_ip=ssh_ip,
                        ssh_port=ssh_port,
                        note=note
                    )
                    server.server_group.add(server_group)
            result = {'code': 200, 'msg': '成功导入{}！'.format(excel_file_obj)}
        except Exception as e:
            print(e)
            result = {'code': 500, 'msg': '导入异常！%s' % e}
        return Response(result)


class AliyunCloudView(APIView):
    """
    阿里云相关接口操作
    """
    def post(self, request):
        request_type = request.data.get('request_type')
        print(request_type)
        if request_type == "getRegion":
            """
            返回所有区域（region）
            """
            secret_id = request.data.get('secret_id')
            secret_key = request.data.get('secret_key')
            cloud = AliCloud(secret_id, secret_key)
            region_result = cloud.region_list()
            code = region_result['code']
            if code == 200:
                # 二次处理，固定字段名
                region = []
                for r in region_result['data']['Regions']['Region']:
                    region.append({"region_id": r['RegionId'], 'region_name': r['LocalName']})
                res = {'code': code, 'msg': '获取区域列表成功！', 'data': region}
            else:
                res = {'code': code, 'msg': region_result['msg']}
            return Response(res)

        elif not request_type == "getRegion":
            # print("创建云主机")
            # 创建云主机信息
            # 凭据、IDC机房、主机分组、SSH连接地址（IP、端口）
            secret_id = request.data.get('secret_id')
            secret_key = request.data.get('secret_key')
            server_group_id_list = request.data.get('server_group')
            region_id = request.data.get('region')  # 区域用于机房里的城市
            ssh_ip = request.data.get('ssh_ip')  # 用户选择使用内网（private）还是公网（public），下面判断对应录入
            ssh_port = int(request.data.get('ssh_port'))
            cloud = AliCloud(secret_id, secret_key)
            instance_result = cloud.instance_list(region_id)

            instance_list = []
            if instance_result['code'] == 200:
                instance_list = instance_result['data']['Instances']['Instance']

                if len(instance_list) == 0:
                    res = {'code': 500, 'msg': '该区域未发现云主机，请重新选择！'}
                    return Response(res)
            elif instance_result['code'] == 500:
                res = {'code': 500, 'msg': '%s' % instance_result['msg']}
                return Response(res)

            # InstanceSet中可用区字段值是英文，例如 ap-beijing-1
            # 先获取可用区英文与中文对应，下面遍历主机再获取中文名
            zone_result = cloud.zone_list(region_id)

            zone_dict = {}
            for z in zone_result['data']['Zones']['Zone']:
                zone_dict[z['ZoneId']] = z['LocalName']

            # 获取主机所在可用区
            # 可用区用于机房里的机房名称
            zone_set = set()
            for host in instance_list:
                zone = host['ZoneId']  # 可用区，例如 ap-beijing-1
                zone_set.add(zone_dict[zone])  # 获取中文名

            # 根据可用区创建机房
            for zone in zone_set:
                # 如果存在不创建
                idc = Idc.objects.filter(name=zone)
                if not idc:
                    city = ""
                    region_list = cloud.region_list()['data']['Regions']['Region']
                    for r in region_list:  # 获取区域对应中文名
                        if r['RegionId'] == region_id:
                            city = r['LocalName']
                    Idc.objects.create(
                        name=zone,
                        city=city,
                        provider="阿里云"
                    )

            # 导入云主机信息到数据库
            for host in instance_list:
                zone = host['ZoneId']
                instance_id = host['InstanceId']  # 实例ID
                # hostname = host['HostName']
                instance_name = host['InstanceName']  # 机器名称
                os_version = host['OSName']

                private_ip_list = host['NetworkInterfaces']['NetworkInterface'][0]['PrivateIpSets']['PrivateIpSet']
                private_ip = []
                for ip in private_ip_list:
                    private_ip.append(ip['PrivateIpAddress'])

                public_ip = host['PublicIpAddress']['IpAddress']
                cpu = "%s核" % host['Cpu']
                memory = "%sG" % (int(host['Memory']) / 1024)

                # 硬盘信息需要单独获取
                disk = []
                disk_list = cloud.instance_disk(instance_id)['data']['Disks']['Disk']
                for d in disk_list:
                    disk.append({'device': d['Device'], 'size': '%sG' % d['Size'], 'type': None})

                create_date = time.strftime("%Y-%m-%d",time.strptime(host['CreationTime'] , "%Y-%m-%dT%H:%MZ"))
                 # 2022-01-30T04:51Z 需要转换才能存储
                expired_time = time.strftime("%Y-%m-%d %H:%M:%S",time.strptime(host['ExpiredTime'], "%Y-%m-%dT%H:%MZ"))

                # 创建服务器
                idc_name = zone_dict[zone]
                idc = Idc.objects.get(name=idc_name) # 一对多

                if ssh_ip == "public":
                    ssh_ip = public_ip[0]
                elif ssh_ip == "private":
                    ssh_ip = private_ip[0]

                data = {'idc': idc,
                        'name': instance_id,
                        'hostname': instance_name,
                        'ssh_ip': ssh_ip,
                        'ssh_port': ssh_port,
                        'machine_type': 'cloud_vm',
                        'os_version': os_version,
                        'public_ip': public_ip,
                        'private_ip': private_ip,
                        'cpu_num': cpu,
                        'memory': memory,
                        'disk': disk,
                        'put_shelves_date': create_date,
                        'expire_datetime': expired_time,
                        'is_verified': 'verified'}
                # 如果instance_name不存在才创建
                server = Server.objects.filter(hostname=instance_name)
                if not server:
                    server = Server.objects.create(**data)
                    # 分组多对多
                    for group_id in server_group_id_list:
                        group = ServerGroup.objects.get(id=group_id)  # 根据id查询分组
                        server.server_group.add(group)  # 将服务器添加到分组
                else:
                    res = {'code': 500, 'msg': '该主机已存在: %s' % instance_name}
                    return Response(res)
            res = {'code': 200, 'msg': '导入云主机成功'}
            return Response(res)


class IdcDashboardView(APIView):
    """
    返回IDC机房数据服务器最多的TOP10
    """
    def get(self, request):
        idc_res = []
        idc_list = []
        server = Server.objects.all()
        for host in server:
            idc = host.idc.name
            provider = host.idc.provider
            idc_list.append(idc + "-" + provider)
        idc_set = set(idc_list)
        for idc_name in idc_set:
            idc_res.append((idc_name, idc_list.count(idc_name)))
        result = sorted(idc_res, key=lambda idc_type: idc_type[1], reverse=True)
        result = result[0:5] #  [[name,number],[],....]
        res = {"code": 200, "msg": "idc TOP10 数据获取成功！", "data": result}
        return Response(res)


class ServerDashboardView(APIView):
    """
    获取主机在线和离线的数量
    """
    def get(self, request):
        online = 0
        offline = 0
        server_query = Server.objects.all()
        for host in server_query:
            if host.is_verified == "verified":
                online += 1
            else:
                offline += 1
        data = [{"value": online, "name": "在线主机"}, {"value": offline, "name": "离线主机"}]
        res = {"code": 200, "msg": "获取主机状态数据成功!", "data": data}
        return Response(res)



