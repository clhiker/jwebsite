from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from user.tools import Tools
from user.dml_user import MysqlDML
from user.ddl_user import FileDDL
# Create your views here.
verification_code = ''
tools = Tools()
dml_user = MysqlDML()
ddl_user = FileDDL()


@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        info = dml_user.queryUser(username, password)
        if info['res'] == 'up200':
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
        email = request.POST.get('email')
        input_verification_code = request.POST.get('verification_code')
        if input_verification_code != verification_code:
            return JsonResponse({'res': "邮箱验证码出错，请重新验证"})

        info = dml_user.addUser(username, password, email)
        if info['res'] == 're200':
            request.session['username'] = username
            request.session['is_login'] = True
            # 建立一个以其名称命名的表
            ddl_user.createTable(username)
            return render(request, 'login.html')
        print(info)
        return JsonResponse(info)

    else:
        return render(request, 'register.html')


def verifyEmail(request):
    global verification_code
    # verification_code = '9527'
    verification_code = tools.getRandomVerificationCode()
    email = request.GET.get('email')
    print(email)
    tools.sendEmail(verification_code, email)
    return render(request, 'register.html')


@csrf_exempt
def logout(request):
    request.session.clear()
    return HttpResponse('')


# def findPassword(request):
#     new_password = tools.getRandomPassword()
#     sendEmail(new_password)
#     username = request.session['username']
#     dml_user.updatePassword(username, new_password)
#     return JsonResponse({'res': '请至邮箱查收新密码'})


def deleteUser(request):
    pass


