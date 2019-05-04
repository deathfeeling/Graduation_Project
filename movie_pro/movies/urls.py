from django.urls import path
from movies import views


urlpatterns = [
    # path('create_moviedata_to_mysql/', views.create_moviedata_to_mysql),   #　创建数据到mysql
    path('classification/<int:classification_id>/', views.classification, name='classification'),  # 电影分类
    path('single/<int:id>/', views.single, name='single'),  # 电影详情
    path('news/', views.news, name='news'),   # 资讯
    path('news_single/', views.news_single, name='news_single'),  # 资讯详情
    path('list/', views.list, name='list'),    # a-z表
    path('contact/', views.contact, name='contact'),    # 联系我
    path('search/', views.search, name='search'),    # 搜索
]