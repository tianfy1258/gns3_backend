from django.db import models


class User(models.Model):
    # 用户id (主键)
    user_id = models.AutoField(primary_key=True)
    # 用户名 (唯一)
    username = models.CharField(max_length=255, unique=True)
    # 密码
    password = models.CharField(max_length=255, default='123456')
    # 用户权限 [user, manager]
    user_auth = models.CharField(max_length=255, default='user')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 修改时间
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True,
        db_table = "user"


