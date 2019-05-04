import json

from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

from movies.models import *
from user.views import top_movies


def create_moviedata_to_mysql(request):
    """创建数据到mysql"""
    with open('result.json', 'r', encoding='utf-8') as f:
        results = f.read()
    results = json.loads(results)
    for item in results:
        title = item['title']
        actor = item['actor']
        language = item['language']
        director = item['director']
        release_date = item['release_date']
        update_date = item['update_date']
        score = item['score']
        synopsis = item['synopsis']
        download_name = item['download_name']
        download_size = item['download_size']
        download_thunder = item['download_thunder']
        TbMovie.objects.create(title=title, actor=actor, language=language, director=director, release_date=release_date,
                               update_date=update_date, score=score, synopsis=synopsis, download_name=download_name,
                               download_size=download_size, download_thunder=download_thunder)
    return HttpResponse('Create successful!')


def classification(request, classification_id):
    """电影分类 分页传入参数page"""
    page = int(request.GET.get('page', 1))     # 页数
    classification = TbClassification.objects.filter(id_classification=classification_id).first()
    classification_name = classification.classification
    movies = classification.tbmovie_set.all()
    paginator = Paginator(movies, 10)   # 每页10条数据
    items = paginator.page(page)
    result = []
    for item in items:
        item = {'id': item.m_id, 'title': item.title,
                'release_date': item.release_date, 'main_pic': item.main_pic}
        result.append(item)
    # 热门数据
    top_movies_data = top_movies(8)
    return render(request, 'classification.html', {'classification': classification_name, 'movies': result,
                                                   'items': items, 'top_movies': top_movies_data,
                                                   'classification_id': classification_id})


def single(request, id):
    """电影详情"""
    movie = TbMovie.objects.filter(m_id=id).first()
    if movie:
        movie_info = movie.__dict__
        movie_info['actor'] = '/'.join(eval(movie_info['actor']))
        movie_info['classifications']= '/'.join([item.classification.upper()
                                                 for item in movie.classification.all()])
        return render(request, 'single.html', movie_info)
    return HttpResponse('Get some wrong!')


def news(request):
    """资讯"""
    return render(request, 'news.html')


def news_single(request):
    """资讯详情"""
    return render(request, 'news-single.html')


def list(request):
    """a-z字母表"""
    return render(request, 'list.html')


def contact(request):
    """联系我"""
    return render(request, 'contact.html')


def search(request):
    """搜索"""
    return 'ok'