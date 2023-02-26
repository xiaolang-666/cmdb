from django.db import models
from system_config.models import Credential


class Idc(models.Model):
    name = models.CharField(max_length=30, verbose_name="机房名称")
    city = models.CharField(max_length=20, verbose_name="城市")
    provider = models.CharField(max_length=30, verbose_name="运营商")
    note = models.TextField(blank=True, null=True, verbose_name="备注")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "cmdb_idc"
        verbose_name_plural = "IDC机房"
        ordering = ('-id',)
        unique_together = ("name", "city")  # 机房名称和城市联合唯一

    def __str__(self):
        return self.name


class ServerGroup(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="分组名称")
    note = models.TextField(blank=True, null=True, verbose_name="备注")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "cmdb_server_group"
        verbose_name_plural = "主机分组"
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Server(models.Model):
    idc = models.ForeignKey(Idc, on_delete=models.PROTECT, verbose_name="IDC机房")
    server_group = models.ManyToManyField(ServerGroup, default="Default", verbose_name="主机分组")
    name = models.CharField(max_length=30, blank=True, verbose_name="名称")
    hostname = models.CharField(max_length=30, unique=True, verbose_name="主机名")
    ssh_ip = models.GenericIPAddressField(verbose_name="SSH IP")  # ip专用字段
    ssh_port = models.IntegerField(verbose_name="SSH端口")
    credential_id = models.ForeignKey(Credential, on_delete=models.PROTECT, verbose_name="凭据ID", null=True,
                                      db_column='credential_id')
    note = models.TextField(blank=True, null=True, verbose_name="备注")

    machine_type = models.CharField(max_length=30, blank=True,
                                    choices=(('vm', '虚拟机'), ('cloud_vm', '云主机'), ('physical_machine', '物理机')),
                                    verbose_name="机器类型")
    os_version = models.CharField(max_length=50, blank=True, null=True, verbose_name="系统版本")
    public_ip = models.CharField(max_length=100, blank=True, null=True, verbose_name="公网IP")
    private_ip = models.JSONField(blank=True, null=True, verbose_name="内网IP")
    cpu_num = models.CharField(max_length=10, blank=True, null=True, verbose_name="CPU")
    cpu_model = models.CharField(max_length=100, blank=True, null=True, verbose_name="CPU型号")
    memory = models.CharField(max_length=30, blank=True, null=True, verbose_name="内存")
    disk = models.JSONField(blank=True, null=True, verbose_name="硬盘")
    put_shelves_date = models.DateField(null=True, blank=True, verbose_name="上架日期")
    off_shelves_date = models.DateField(null=True, blank=True, verbose_name="下架日期")
    expire_datetime = models.DateTimeField(blank=True, null=True, verbose_name="租约过期时间")
    is_verified = models.CharField(max_length=10, blank=True, choices=(('verified', '已验证'), ('unverified', '未验证')),
                                   default='unverified', verbose_name="SSH验证状态")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    class Meta:
        db_table = "cmdb_server"
        verbose_name_plural = "主机管理"
        ordering = ('-id',)

    def __str__(self):
        return self.hostname


class IiotDocument(models.Model):
    # 后续新需求 记录每次历史记录更新的代码 v2版本在考虑
    name = models.CharField(max_length=30, verbose_name="文档名称", unique=True)
    note = models.TextField(blank=True, null=True, verbose_name="文档内容")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    class Meta:
        db_table = "cmdb_document"
        verbose_name_plural = "iiot运维文档"
        ordering = ('-id',)

    def __str__(self):
        return self.name
