import time
import base64
from urllib.parse import quote
from re import fullmatch

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password, make_password
from django_redis import get_redis_connection

from movies.models import *
from movie_pro.settings import RE_USER_PASSWORD, RE_USERNAME, RE_PHONE, RE_EMAIL
from user.tools import gen_mobile_code, send_mobile_code, get_ip_address
from user.tools import gen_captcha_text
from user.captcha import Captcha


@api_view(['GET', 'POST'])
def login(request):
    """登录"""
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('password')
        captcha = request.POST.get('captcha').lower()
        # 验证字段完整性
        if all([user, password, captcha]):
            user = TbUser.objects.filter(username=user).first()
            if not user:
                return JsonResponse({'code': 1001, 'msg': '该用户不存在,请先注册'})
            if not check_password(password, user.password):
                return JsonResponse({'code': 1002, 'msg':'密码输入错误'})
            captcha_truely = request.session.get('code_text').lower()
            if captcha != captcha_truely:
                return JsonResponse({'code': 1003, 'msg':'验证码错误'})
            # 记录登录信息
            ip = get_ip_address(request)   # 拿到用户登录ip
            TbLoginIp.objects.create(ip_addr=ip, login_date=time.strftime("%Y-%m-%d %H:%M:%S", \
                                                                          time.localtime()), u=user)
            # 保持登录会话
            request.session['token'] = user.u_id
            return JsonResponse({'code':200, 'msg':'ok'})
        else:
            return JsonResponse({'code':1000, 'msg':'请填写所有的字段'})


@api_view(['POST'])
def captcha(request):
    """生成图片验证码"""
    # 随机验证码内容, 可以指定长度
    code_text = gen_captcha_text()
    # 将验证码放入session缓存中
    request.session['code_text'] = code_text
    # instance()指定验证码宽高； generate(code_text)生成验证码,返回图片二进制数据
    code_bytes = Captcha.instance().generate(code_text)
    code_base64_str = base64.b64encode(code_bytes).decode('utf-8')
    return JsonResponse({'code':200, 'pic':code_base64_str})


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
        # 注册用户状态默认为1(可用)
        TbUser.objects.create(username=username, password=password, email=email,
                              phone=phone, register_date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                              register_ip=ip_addr, u_status=1)
        # 注册成功删除缓存验证码信息
        cli.delete(f'mobile_code:{phone}')
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


def logout(request):
    """注销"""
    del request.session['token']
    return HttpResponseRedirect(reverse('user:login'))


def request_user_info(request):
    """请求用户登录信息"""
    user_id = request.session.get('token')
    if user_id:
        user = TbUser.objects.get(pk=user_id)
        name = user.username
        return JsonResponse({'code':200, 'user':{'id':user_id, 'name':name}})
    else:
        return JsonResponse({'code':1050, 'user':{'id':0, 'name':'未登录'}})


def index(request):
    """主页"""
    latest_movies_data = latest_movies(8)
    top_movies_data = top_movies(8)
    return render(request, 'index.html', {'latest_movies': latest_movies_data, 'top_movies': top_movies_data})


def latest_movies(filter_number):
    """最新电影: filter参数指定获取多少条数据,默认全部"""
    movies = TbMovie.objects.order_by('-release_date').only('m_id', 'title', 'release_date', 'main_pic')
    movies = movies[:int(filter_number)]
    result = []
    for movie in movies:
        release_date = movie.release_date
        release_date = f'{release_date.year}年{release_date.month}月{release_date.day}日'
        item = {'id': movie.m_id, 'title': movie.title,
                'release_date': release_date, 'main_pic': movie.main_pic}
        result.append(item)
    return result


def top_movies(filter_number):
    """排行榜电影: filter参数指定获取多少条数据,默认全部"""
    movies = TbMovie.objects.order_by('-score').only('m_id', 'title', 'release_date', 'main_pic')
    movies = movies[:int(filter_number)]
    result = []
    for movie in movies:
        release_date = movie.release_date
        release_date = f'{release_date.year}年{release_date.month}月{release_date.day}日'
        item = {'id': movie.m_id, 'title': movie.title,
                'release_date': release_date, 'main_pic': movie.main_pic}
        result.append(item)
    return result