from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.http import HttpResponse


from .models import *

"""
    Возвращает список материала, можно отсортировать по дате добавления    
"""


def index(request):
    posts = Posts.objects.all()
    return render(request, 'like/index.html', {'posts': posts})


"""
    Функция add_comment на вход принимает 3 параметра, uid-пользователь (в будущем uid будет подтягиваться
    из сессии), pid - это id материала, к которому оставили комментарий (так же в будущем можно рассмотреть
    ситуацию, когда надо будет ответить на комментарий), text - сам комментарий. Функция создает запись
    в таблице Comments и возвращает id записи.
"""


def add_comment(request):
    if request.method == "POST":
        # Ожидается, что пользователь будет авторизован и его uid можно подтянуть из сессии
        data = JSONParser().parse(request)
        result = Comments.create_comment(pid=int(data['pid']), uid=int(data['uid']),  comment=data['text'])
        response = HttpResponse(content_type='application/json')
        response.content = result
        return response


"""
    Функция vote на вход принимает 4 параметра, uid - id пользователя, variety - определяет, что это
    комментарий или материал, mid - id комментария или материала, value - голос, (1 или -1). Функция
    возвращает id при удачно записи. Если запись уже существует, то он перезаписывает голос.
"""


def vote(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        result = Users.vote(uid=int(data['uid']), material_id=int(data['mid']),
                            variety=data['variety'], value=data['value'])
        response = HttpResponse(content_type='application/json')
        response.content = result
        return response


"""
    Функция ratings на вход принимает 1 параметр, pid - id материала (в будущем можно доделать и возвращать
    оценки для комментариев). Возвращает плюсы/минусы/общее количество голосов в разрезе материала.    
"""


def ratings(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        result = Posts.get_ratings(data['pid'])
        response = HttpResponse(content_type='application/json')
        response.content = result
        return response
