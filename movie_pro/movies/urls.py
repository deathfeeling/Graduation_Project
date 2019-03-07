from django.urls import path
from movies import views


urlpatterns = [
    # path('create_moviedata_to_mysql/', views.create_moviedata_to_mysql),   #　创建数据到mysql
    path('classification/', views.classification, name='classification'), # 电影分类
    path('single/<int:id>/', views.single, name='single'),  # 电影详情
    path('news/', views.news, name='news'),   # 资讯
    path('list/', views.list, name='list'),    # a-z表
    path('contact/', views.contact, name='contact'),    # 联系我
]