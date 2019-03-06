from django.urls import path
from movies import views

urlpatterns = [
    path('create_moviedata_to_mysql/', views.create_moviedata_to_mysql),
    path('classification/', views.classification, name='classification'), # 电影分类
    path('series/', views.series, name='series'),   # 电视剧
    path('news/', views.news, name='news'),   # 资讯
    path('list/', views.list, name='list'),    # a-z表
    path('contact/', views.contact, name='contact'),    # 联系我
]