from django.db import models


class Credential(models.Model):
    auth_choice = (
        (1, "密码"),
        (2, "秘钥")
    )
    name = models.CharField(max_length=30, verbose_name="凭据名称")
    username = models.CharField(max_length=20, verbose_name="用户名")
    auth_mode = models.IntegerField(choices=auth_choice, default=1, verbose_name="认证方式")
    password = models.CharField(max_length=50, blank=True, verbose_name="密码")
    private_key = models.TextField(blank=True, verbose_name="私钥")
    note = models.TextField(blank=True, verbose_name="备注")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "system_config_credential"
        verbose_name_plural = "凭据管理"
        ordering = ('-id',)

    def __str__(self):
        return self.name
