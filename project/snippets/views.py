from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
#
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializers import SnippetSerializer

# Create your views here.
class JSONResponse(HttpResponse):
    """
    콘텐츠(data)를 JSON으로 변환한 후 , HttpResponse 형태로 반환함.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content,**kwargs)


@csrf_exempt
def snippet_list(request) -> JSONResponse:
    """
    :param request: request 객체.
    :return: JSONResponse
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid(): # 시리얼라이저의 유효성 검사를 통과하면.
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk) -> JSONResponse:
    """
    코드 조각 조회, 업데이트, 삭제
    :param request: request객체
    :param pk: pk넘버
    :return: JSONResponse
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist: # objects.get은 값이 없으면 DoesNotExist에러를 일으킨다.
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JSONResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)
    elif request.method =='DELETE':
        snippet.delete()
        return HttpResponse(status=204)
