import json
import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from pypinyin import pinyin

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
        release_date = item.release_date
        release_date = f'{release_date.year}年{release_date.month}月{release_date.day}日'
        item = {'id': item.m_id, 'title': item.title,
                'release_date': release_date, 'main_pic': item.main_pic}
        result.append(item)
    # 热门数据
    top_movies_data = top_movies(8)
    return render(request, 'classification.html', {'classification': classification_name, 'movies': result,
                                                   'items': items, 'top_movies': top_movies_data,
                                                   'classification_id': classification_id})


@api_view(['GET', 'POST'])
def single(request, id):
    """电影详情"""
    movie = TbMovie.objects.filter(m_id=id).first()
    if request.method == 'GET':
        if movie:
            movie_info = movie.__dict__
            movie_info['release_date'] = f'{movie_info["release_date"].year}年{movie_info["release_date"].month}月{movie_info["release_date"].day}日'
            movie_info['actor'] = movie_info['actor']
            movie_info['classifications'] = '/'.join([item.classification.upper()
                                                     for item in movie.classification.all()])
            # 获取该电影下的评论信息
            comment_info = []
            for item in movie.tbcomment_set.order_by('-comment_date').all():
                comment_temp = dict()
                comment_temp['username'] = item.id_user.username
                comment_temp['comment'] = item.comment
                comment_temp['comment_date'] = item.comment_date.strftime('%Y-%m-%d %H:%M:%S')
                comment_info.append(comment_temp)
            movie_info['comment_info'] = comment_info
            return render(request, 'single.html', movie_info)
        return HttpResponse('Get some wrong!')
    if request.method == 'POST':
        # 提交评论
        data = request.POST.dict()
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        message = data.get('message')
        user = TbUser.objects.filter(username=name, phone=phone, email=email).first()
        if user:
            comment = TbComment.objects.create(comment=message, comment_date=datetime.datetime.now())
            comment.id_user = user
            comment.m = movie
            comment.save()
            return HttpResponseRedirect(f'/movies/single/{id}/')
        return HttpResponse('用户不存在，不能进行评论！')


def news(request):
    """资讯"""
    page = int(request.GET.get('page', 1))     # 页数
    props = ('n_id', 'title', 'less_content', 'news_date')
    news = TbNews.objects.all().only(*props).select_related().order_by('-news_date')
    paginator = Paginator(news, 4)   # 每页4条数据
    news = paginator.page(page)
    data = []
    for new in news:
        item = new.__dict__
        item['news_date'] = item['news_date'].strftime('%Y-%m-%d %H:%M:%S')
        data.append(dict(item, **{'movie_title': new.m.title, 'movie_id': new.m.m_id}))
    return render(request, 'news.html', {'data': data, 'news': news})


def news_single(request, news_id):
    """资讯详情"""
    news = TbNews.objects.filter(n_id=news_id).select_related().first()
    item = news.__dict__
    item['news_date'] = item['news_date'].strftime('%Y-%m-%d %H:%M:%S')
    data = dict(item, **{'movie_pic': news.m.pic, 'movie_title': news.m.title, 'movie_id': news.m.m_id})
    return render(request, 'news-single.html', {'data': data})


def list(request):
    """a-z字母表"""
    query_number = request.GET.get('query_number')
    movies = TbMovie.objects.order_by('-score').all()
    if query_number:
        # 查询首字母
        movies_info = []   # 符合条件电影
        counter = 1
        for movie in movies:
            if pinyin(movie.title)[0][0][0] == query_number:
                movie_info = movie.__dict__
                movie_info['counter'] = counter
                movie_info['release_date'] = movie_info["release_date"].year
                movie_info['country'] = movie.id_region.region
                movie_info['classifications'] = '/'.join([item.classification.upper()
                                                          for item in movie.classification.all()])
                movies_info.append(movie_info)
                counter += 1
    else:
        # 所有电影
        movies_info = [dict(movie.__dict__, **({'counter': counter + 1,
                                                'release_date': movie.release_date.year,
                                                'country': movie.id_region.region,
                                                'classifications': '/'.join([item.classification.upper()
                                                    for item in movie.classification.all()])}))
                       for counter, movie in enumerate(movies)]
    return render(request, 'list.html', locals())


@api_view(['GET', 'POST'])
def contact(request):
    """联系我"""
    if request.method == 'GET':
        return render(request, 'contact.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        user = TbUser.objects.filter(username=username, phone=phone, email=email).first()
        if user:
            suggestion = TbSuggestion.objects.create(message=message, submit_date=datetime.datetime.now(), u=user)
            suggestion.save()
            return HttpResponse('Send Success')
        return HttpResponse('用户不存在，不能提交意见！')


@api_view(['POST'])
def search(request):
    """搜索"""
    search = request.POST.get('search')
    if not search:
        return HttpResponse('Please input keywords!')
    movies = TbMovie.objects.filter(title__contains=search).order_by('-score').all()
    movies_info = []
    for counter, movie in enumerate(movies):
        movie_info = movie.__dict__
        movie_info['counter'] = counter + 1
        movie_info['release_date'] = movie_info["release_date"].year
        movie_info['country'] = movie.id_region.region
        movie_info['classifications'] = '/'.join([item.classification.upper()
                                                    for item in movie.classification.all()])
        movies_info.append(movie_info)
    return render(request, 'list.html', locals())