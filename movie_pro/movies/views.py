import json

from django.http import HttpResponse
from django.shortcuts import render

from movies.models import TbMovie


def create_moviedata_to_mysql(request):
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


