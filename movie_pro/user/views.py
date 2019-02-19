import time
from hashlib import md5
from re import fullmatch

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password, make_password
from django_redis import  get_redis_connection
from django.http import JsonResponse

from movies.models import TbUser
from movie_pro.settings import RE_USER_PASSWORD, RE_USERNAME, RE_PHONE, RE_EMAIL
from user.tools import gen_mobile_code, send_mobile_code, get_ip_address


@api_view(['GET', 'POST'])
def login(request):
    """登录"""
    # todo:1、记录登录ip信息； 2、记录登录会话 ；3、调出登录验证码
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('password')
        if all([user, password]):
            user = TbUser.objects.filter(username=user).first()
            if not user:
                return JsonResponse({'code': 1001, 'msg': '该用户不存在'})
            if not check_password(password, user.password):
                return JsonResponse({'code': 1002, 'msg':'密码输入错误'})
            return JsonResponse({'code':200, 'msg':'ok'})
        else:
            return JsonResponse({'code':1000, 'msg':'用户名或密码不能为空'})


@api_view(['GET', 'POST'])
def register(request):
    """注册"""
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        password2 = request.POST.get('cpwd')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        phone_code = request.POST.get('phone_code')
        # 验证字段信息是否完整
        if not all([username, password, password2, phone, email, phone_code]):
            return JsonResponse({'code':1004, 'msg':'请完整填写所有字段'})
        if not fullmatch(RE_USERNAME, username):
            return JsonResponse({'code':1005, 'msg':'用户名长度4-12位，包含字母数字下划线'})
        if not fullmatch(RE_USER_PASSWORD, password):
            return JsonResponse({'code':1007, 'msg':'密码长度6-12位，必须包含字母和数字'})
        if password2 != password:
            return JsonResponse({'code':1006, 'msg':'两次密码不同'})
        if not fullmatch(RE_EMAIL, email):
            return JsonResponse({'code':1009, 'msg':'请输入正确的邮箱地址'})
        if not fullmatch(RE_PHONE, phone):
            return JsonResponse({'code':1008, 'msg':'请输入正确的手机号码'})
        cli = get_redis_connection(alias='default')
        phone_code_truely = cli.get(f'mobile_code:{phone}')
        if not phone_code_truely:
            return JsonResponse({'code':1011, 'msg':'请先点击发送，获取验证码'})
        if phone_code_truely.decode('utf-8') != phone_code:
            return JsonResponse({'code': 1010, 'msg':'验证码不正确,请稍后重试！'})
        user = TbUser.objects.filter(username=username).only('username').first()
        if user:
            return JsonResponse({'code':1012, 'msg':'该用户已存在'})
        # 创建用户信息
        ip_addr = get_ip_address(request)
        password = make_password(password)
        TbUser.objects.create(username=username, password=password, email=email, phone=phone, register_date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), register_ip=ip_addr, u_status=1)
        return JsonResponse({'code':200, 'msg':'ok'})


def click_send_button(request, mobile):
    """发送手机验证码"""
    cli = get_redis_connection(alias='default')
    if cli.get(f'mobile_code:{mobile}'):
        return JsonResponse({'code': 20000, 'msg': '请不要在120s内重复发送手机验证码'})
    code = gen_mobile_code(length=6)
    cli.set(f'mobile_code:{mobile}', code, ex=120)
    result = send_mobile_code(code=code, mobile=mobile)
    # {'return_code': '00000', 'order_id': 'MB1550561278181631021'}
    return JsonResponse(result)


def index(request):
    return render(request, 'index.html')