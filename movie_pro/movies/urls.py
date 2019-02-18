from django.urls import path
from movies import views

urlpatterns = [
    path('create_moviedata_to_mysql/', views.create_moviedata_to_mysql, name='create_moviedata_to_mysql'),
]