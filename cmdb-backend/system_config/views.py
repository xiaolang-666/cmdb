from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from system_config.serializers import CredentialSerializer
from system_config.models import Credential


class CredentialViewSet(ModelViewSet):
    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]  # 指定过滤器
    search_fields = ('name',)  # 指定可搜索的字段

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
        result = {"code": 200, "msg": "凭据更新成功", "data": serializer.data}
        return Response(result)

    def create(self, request, *args, **kwargs):
        credential = Credential.objects.filter(name=request.data.get('name'))
        if not credential:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            res = {'code': 200, 'msg': '凭据创建成功'}
        else:
            res = {'code': 500, 'msg': '该凭据已存在！'}
        return Response(res)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except Exception as e:
            print(e)
            result = {"code": 500, "msg": "改凭据绑定了其他主机不允许删除！"}
            return Response(result)
        result = {"code": 200, "msg": "删除凭据成功！"}
        return Response(result)

    def perform_destroy(self, instance):
        instance.delete()
