from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest, DescribeInstancesRequest, \
    DescribeZonesRequest, DescribeDisksRequest
import json


class AliCloud:
    def __init__(self, secret_id, secret_key):
        self.secret_id = secret_id
        self.secret_key = secret_key

    def region_list(self):
        """
        所有区域列表
        """
        client = AcsClient(self.secret_id, self.secret_key)
        req = DescribeRegionsRequest.DescribeRegionsRequest()  # 获取地区
        try:
            resp = client.do_action_with_exception(req)
            resp = json.loads(resp.decode())
            resp = {'code': 200, 'data': resp}
            return resp
        except Exception as e:
            return {'code': 500, 'msg': "获取地区列表失败！%s" % e}

    def zone_list(self, region_id):
        """
        可用区列表
        """
        client = AcsClient(self.secret_id, self.secret_key)
        req = DescribeZonesRequest.DescribeZonesRequest()
        req.add_query_param('RegionId', region_id)
        try:
            resp = client.do_action_with_exception(req)
            resp = json.loads(resp.decode())
            resp = {'code': 200, 'data': resp}
            return resp
        except Exception as e:
            print("获取可用区列表失败: %s" % e)
            return {'code': 500, 'msg': "获取可用区列表失败: %s" % e}

    def instance_list(self, region_id):
        """
        主机实例列表
        """
        client = AcsClient(self.secret_id, self.secret_key)
        req = DescribeInstancesRequest.DescribeInstancesRequest()
        req.add_query_param('RegionId', region_id)
        try:
            resp = client.do_action_with_exception(req)
            resp = json.loads(resp.decode())
            resp = {'code': 200, 'data': resp}
            return resp
        except Exception as e:
            print("获取实例失败：%s" % e)
            return {'code': 500, 'msg': "获取实例失败：%s" % e}

    def instance_disk(self, instance_id):
        client = AcsClient(self.secret_id, self.secret_key)
        req = DescribeDisksRequest.DescribeDisksRequest()
        req.add_query_param('InstanceId', instance_id)
        try:
            resp = client.do_action_with_exception(req)
            resp = json.loads(resp.decode())
            resp = {'code': 200, 'data': resp}
            return resp
        except Exception as e:
            print("获取磁盘实例失败：%s" % e)
            return {'code': 500, 'msg': "获取磁盘实例失败：%s" % e}
