from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from user.models import User

# Create your views here.


@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        info = MysqlDML().queryUser(username, password)
        if info['result'] == 'up200':
            request.session['username'] = username
            request.session['is_login'] = True
        return JsonResponse(info)

    else:
        return render(request, 'login.html')


@csrf_exempt
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        info = MysqlDML().addUser(username, password)
        if info['result'] == 're200':
            request.session['username'] = username
            request.session['is_login'] = True
        return JsonResponse(info)

    else:
        return render(request, 'register.html')


def logout(request):
    request.session.clear()
    return HttpResponse('')


class DML:
    def __init__(self):
        pass


class MysqlDML(DML):
    def queryUser(self, username, password):
        username_db = User.objects.filter(username=username)
        if not username_db.exists():
            return {'result': "用户名不存在"}
        else:
            password_in_db = User.objects.get(username=username)
            if password != password_in_db.password:
                return {'result': "密码不正确"}
            else:
                return {'result': "up200"}

    def addUser(self, username, password):
        username_db = User.objects.filter(username=username)
        if username_db.exists():
            return {'result': "用户名已存在"}
        else:
            User.objects.create(username=username, password=password)
            return {'result': "re200"}
