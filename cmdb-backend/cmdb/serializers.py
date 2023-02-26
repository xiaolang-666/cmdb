from cmdb.models import Idc, ServerGroup, Server, IiotDocument
from rest_framework import serializers


class IdcSerializer(serializers.ModelSerializer):
    """
    IDC机房序列化类
    """

    class Meta:
        model = Idc
        fields = "__all__"
        read_only_fields = ("id",)  # 仅用于序列化（只读）字段，反序列化（更新）可不传


class IiotDocumentSerializer(serializers.ModelSerializer):
    """
    运维文档序列化类
    """

    class Meta:
        model = IiotDocument
        fields = "__all__"
        read_only_fields = ("id",)  # 仅用于序列化（只读）字段，反序列化（更新）可不传


class ServerGroupSerializer(serializers.ModelSerializer):
    """
    主机分组序列化类
    """

    class Meta:
        model = ServerGroup
        fields = "__all__"
        read_only_fields = ("id",)


class ServerSerializer(serializers.ModelSerializer):
    """
    服务器序列化类
    """
    idc = IdcSerializer(read_only=True)  # 一对多 拿到机房的详情数据 可以完整显示idc所有的数据 不仅限于id
    server_group = ServerGroupSerializer(read_only=True, many=True)  # 多对多 拿到分组的详情数据 可以完整显示分组所有的数据 不仅限于id

    class Meta:
        model = Server
        fields = "__all__"
        read_only_fields = ("id",)
