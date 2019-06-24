from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@csrf_exempt
def home(request):
    if request.method == "GET":
        return render(request, 'home.html')

    elif request.method == "POST":
        return render(request, 'home.html')
        # from_city = request.POST.get('station')
        # print(from_city)
        #
        # if plane_time.getRouteHTML():
        #     return JsonResponse({'res': 'ok'})
        # else:
        #     return JsonResponse({'res': 'ok'})
    else:
        return render(request, 'home.html')


def header(request):
    return render(request, 'header.html')