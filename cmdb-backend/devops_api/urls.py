from django.contrib import admin
from django.urls import path, include, re_path
from cmdb.views import IdcViewSet, ServerGroupViewSet, ServerViewSet, HostCollectView, CreateHostView, \
    ExcelCreateHostView, AliyunCloudView, IdcDashboardView, ServerDashboardView, IiotOpsDocumentView
from rest_framework import routers
from system_config.views import CredentialViewSet
from libs import token_auth


urlpatterns = [
    path('admin/', admin.site.urls),  # admin管理
    path('api/cmdb/host_collect/', HostCollectView.as_view()),  # 采集主机信息
    re_path('^api/login/$', token_auth.CustomAuthToken.as_view()),  # 登录
    re_path("^api/change_password/$", token_auth.ChangeUserPasswordView.as_view()),  # 修改密码
    re_path('^api/cmdb/create_host/$', CreateHostView.as_view()),  # 新建主机
    re_path('^api/cmdb/excel_create_host/$', ExcelCreateHostView.as_view()),  # Excel导入
    re_path('^api/cmdb/aliyun_cloud/$', AliyunCloudView.as_view()),  # 阿里云主机导入
    re_path('^api/cmdb/idc_dashboard/$', IdcDashboardView.as_view()),  # Idc仪表板
    re_path('^api/cmdb/server_dashboard/$', ServerDashboardView.as_view()),  # Idc仪表板

]
router = routers.DefaultRouter()
router.register(r'idc', IdcViewSet, basename="idc")  # idc视图
router.register(r'server_group', ServerGroupViewSet, basename="server_group")  # 服务器分组视图
router.register(r'server', ServerViewSet, basename="server")  # 服务器视图
urlpatterns += [
    path('api/cmdb/', include(router.urls))
]

#  视图集才能使用router来定义 视图要继承ModelViewSet类
router = routers.DefaultRouter()
router.register(r'credential', CredentialViewSet, basename="credential")  # 凭据管理
urlpatterns += [
    path('api/config/', include(router.urls))
]


#  视图集才能使用router来定义 视图要继承ModelViewSet类
router = routers.DefaultRouter()
router.register(r'iiot', IiotOpsDocumentView, basename="iiot_document")  # iiot运维文档管理
urlpatterns += [
    path('api/document/', include(router.urls))
]
