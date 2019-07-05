from django.db import models
# from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(models.Model):
    username = models.CharField('用户名', max_length=40)
    password = models.CharField('密码', max_length=40)
    email = models.CharField('邮箱', max_length=100)


# class File(models.Model):
#     # 主键
#     virtual_path = models.CharField('文件虚拟地址', max_length=256)
#     df_type = models.CharField('类型', max_length=256)
#     name = models.CharField('文件名', max_length=256)
#     size = models.CharField('文件大小', max_length=256)
#     true_path = models.CharField('文件实际地址', max_length=256)
#     change_time = models.CharField('文件修改日期', max_length=256)
#     hash_code = models.CharField('文件哈希', max_length=256)
#     form_type = models.CharField('文件类型', max_length=256)











