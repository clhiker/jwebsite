# from django.contrib.auth.forms import UserCreationForm
# from .models import MyUser
# from django import forms
#
# class MyUserCreationForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(MyUserCreationForm, self).__init__(*args, **kwargs)
#

# -*- coding: utf-8 -*-

from user.models import User


# 数据库操作
class OperateUser:
    def __init__(self):
        pass

    def queryUser(self, username, password):
        user_info = User.objects.all()
        if username not in user_info:
            return "用户名不存在"
        else:
            password_in_db = User.objects.filter(username=username)
            if password != password_in_db:
                return "密码不正确"
            else:
                return "登录成功"


if __name__ == '__main__':
    print(OperateUser().queryUser('clhiker', '7155293'))