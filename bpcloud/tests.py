# # from django.test import TestCase
#
# # Create your tests here.
#
#
# # 动态创建类
# class Father:
#     def __init__(self):
#         self.username = 'username'
#         self.password = 'password'
#         self.email = 'email'
#
#
# def sonF1(self):
#     print(self.username)
#
#
# def sonF2(self):
#     print('sonf2')
#
#
# # 创建一个 my_class 类
# name = 'Son'
# my_class = type(name, (Father,), dict(f1=sonF1, f2=sonF2))
# # 实例化 my_class 类
# h = my_class()
# # 调用 my_class 类的方法
# h.f1()
# h.f2()


# 动态创建类
class Father:
    username = 'username'


# 创建一个 my_class 类
name = 'Son'
my_class = type(name, (Father,), dict())
# 实例化 my_class 类
h = my_class()
print(h.username)