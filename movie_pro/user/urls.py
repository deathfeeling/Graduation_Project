from django.urls import path

from user import views


urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('captcha/', views.captcha, name='captcha'),   # 生成图片验证码
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('click_send_button/<str:mobile>/', views.click_send_button, name='click_send_button'),
]