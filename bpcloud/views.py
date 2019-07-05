import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bpcloud.deal_info import Deal
from bpcloud.dml_hash import DMLHash
# Create your views here.
now_path = '/'
deal = Deal()
dml_hash = DMLHash()
deal.setTable('test')


def home(request):
    return render(request, 'home.html')


def initHome(request):
    username = request.session['username']
    deal.setTable(username)
    line_dict = deal.getPageInfo(now_path)
    print(line_dict)
    return JsonResponse({'res': line_dict})


def queryPageInfo(request):
    global now_path
    name = request.GET.get("name")
    info = request.GET.get("info")
    if info == 'previous':
        if now_path == '/':
            line_dict = deal.getPageInfo(now_path)
        else:
            now_path = now_path[: now_path.rfind('/')-1]
            line_dict = deal.getPageInfo(now_path)
    elif info == 'flush':
        line_dict = deal.getPageInfo(now_path)
    else:
        if name == '/':
            now_path = '/'
        else:
            now_path = now_path + name + '/'
        line_dict = deal.getPageInfo(now_path)

    print(line_dict)
    return JsonResponse({'res': line_dict})


def queryDustbin(request):
    line_dict = deal.getDustbinInfo()
    return JsonResponse(line_dict)


@csrf_exempt
def uploadFile(request):
    virtual_path = request.POST.get("fileName")
    filename = virtual_path[virtual_path.rfind('/')+1:]
    file_size = request.POST.get("fileSize")
    df_type = request.POST.get("fileType")
    keep_time = request.POST.get("fileUploadTime")
    hash_code = request.POST.get("fileHash")
    true_path = './storage/' + hash_code + '.' + filename

    print(virtual_path)
    print(filename)

    upload_file = request.FILES.get("upload-file")
    if upload_file:
        with open(true_path, 'wb+') as f:
            for chunk in upload_file.chunks():  # 分块写入文件
                f.write(chunk)

    dml_hash.addHashFile(file_size, filename, hash_code)

    virtual_path = now_path + virtual_path[:virtual_path.rfind('/')+1]
    print(virtual_path)

    deal.addInfo(virtual_path, filename, file_size,
                 true_path, 'F', keep_time, hash_code, df_type)
    deal.commit()

    return HttpResponse()


@csrf_exempt
def download(request):
    real_path_list = []
    name_list = json.loads(request.POST.get('name_list'))
    for name in name_list:
        real_path = deal.getRealPath(now_path, name)
        if real_path:
            real_path_list.append(real_path)
        else:
            return JsonResponse({'res': 'error'})
    return JsonResponse({
        'res': real_path_list,
    })


def dfileOpera(request):
    opera = request.GET.get('opera')
    info_list = json.loads(request.GET.get('info_list'))
    info = request.GET.get('info')
    if opera == 'recovery':
        for item in info_list:
            name = item['name']
            df_type = item['df_type']
            delete_time = item['delete_time']
            if not deal.operateDFile(opera, now_path, name, delete_time, df_type):
                return JsonResponse({
                    'res': 'error',
                })
    else:
        if info_list is None:
            if not deal.operateDFile(opera, '', '', info, ''):
                return JsonResponse({
                    'res': 'error',
                })
        else:
            for item in info_list:
                name = item['name']
                df_type = item['df_type']
                if not deal.operateDFile(opera, now_path, name, info, df_type):
                    return JsonResponse({
                        'res': 'error',
                    })

    deal.commit()
    return JsonResponse({
        'res': 'res200',
    })


def moveCheck(request):
    info_list = json.loads(request.GET.get('info_list'))
    to_path = request.GET.get('to_path')
    conflict_list = []
    for info in info_list:
        name = info['name']
        df_type = info['df_type']
        if deal.checkConflict(name, df_type, to_path):
            # conflict_list.append((name, df_type))
            conflict_list.append(name)
    if len(conflict_list) == 0:
        return JsonResponse({'res': 'res200'})
    else:
        return JsonResponse({'res': str(conflict_list)+'出现冲突'})


@csrf_exempt
def recoveryCheck(request):
    info_list = json.loads(request.GET.get('info_list'))
    conflict_list = []
    for info in info_list:
        name = info['name']
        df_type = info['df_type']
        delete_time = info['delete_time']
        if deal.checkBeforeRecovery(name, df_type, delete_time):
            conflict_list.append(name)
    if len(conflict_list) == 0:
        return JsonResponse({'res': 'res200'})
    else:
        return JsonResponse({'res': conflict_list})


@csrf_exempt
def hashCheck(request):
    hash_code = request.POST.get('hash_code')
    if dml_hash.queryHash(hash_code):
        return JsonResponse({'res': 'exist'})
    else:
        return JsonResponse({'res': 'not_exist'})




# @csrf_exempt
# def uploadDir(request):
#     file_list = request.FILES.getlist("upload-dir")
#     path_list = request.POST.get('path').split(',')
#     # for item in path_list:
#     #     print(item)
#     for item in file_list:
#         if item:
#             with open('/home/clhiker/storage/' + item.name, 'wb+') as f:
#                 for chunk in item.chunks():  # 分块写入文件
#                     f.write(chunk)
#     return HttpResponse()

# @csrf_exempt
# def upload(request):
#     filename  = request.POST.get("fileName")
#     file_size = request.POST.get("fileSize")
#     df_type = request.POST.get("fileType")
#     keep_time = request.POST.get("fileUploadTime")
#     hash_code = request.POST.get("hashCode")
#     file_data = request.POST.get("data")
#     true_path = './storage/' + filename
#
#     dml_hash.addHashFile(file_size, filename, hash_code)
#     with open(true_path, 'wb+') as f:
#         f.write(file_data)
#
#     deal.addInfo(now_path, filename, file_size, true_path, df_type, keep_time, hash_code)
#
#     return HttpResponse()