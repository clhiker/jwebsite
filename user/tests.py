from django.test import TestCase
from user.models import User


# Create your tests here.
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
    queryUser('clhiker', '7155293')