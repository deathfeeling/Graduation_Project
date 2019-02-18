from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('password')
        if all([user, password]):
            pass
        else:
            return render(request, 'login.html', {'msg': '账号或密码不能为空'})
        return HttpResponseRedirect(reverse('user:index'))


def register(request):
    return render(request, 'register.html')


def index(request):
    return render(request, 'index.html')


