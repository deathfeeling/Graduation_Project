from hashlib import md5

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from rest_framework.decorators import api_view

from movies.models import TbUser


@api_view(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('password')
        if all([user, password]):
            user = TbUser.objects.filter(username=user, password=password).first()
            if not user:
                return JsonResponse({'code': 1001, 'msg': '用户名或密码错误'})
            

        else:
            return JsonResponse({'code':1000, 'msg':'用户名或密码不能为空'})
        return HttpResponseRedirect(reverse('user:index'))


def register(request):
    return render(request, 'register.html')


def index(request):
    return render(request, 'index.html')


