# from django.db import models
# from django.contrib.auth.models import AbstractUser
# Create your models here.


# class MyUser(AbstractUser):
#     username = models.CharField('用户名', max_length=20)
#     password = models.CharField('密码', max_length=20)
#     qq      = models.CharField('QQ号码',  max_length=20)
#     we_chat = models.CharField('微信号码', max_length=20)
#     mobile  = models.CharField('电话号码', max_length=11, unique=True)
#
#     def __str__(self):
#         return self.username


from django.db import models


class User(models.Model):
    username = models.CharField('用户名', max_length=20)
    password = models.CharField('密码', max_length=20)