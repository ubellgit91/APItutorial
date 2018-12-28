from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
#
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
#
from .models import Snippet
from .serializers import SnippetSerializer

# Create your views here.
class JSONResponse(HttpResponse):
    """
    콘텐츠(data)를 JSON으로 변환한 후 , HttpResponse 형태로 반환함.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data) # Renderer 객체 리턴받고, 리턴받은 Renderer의 함수 render()실행
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content,**kwargs)


@api_view(['GET', 'POST'])
@csrf_exempt
def snippet_list(request, format=None) -> JSONResponse:
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


@api_view(['GET', 'PUT', 'DELETE']) # request method가 get, put, delete 일 때에만 해당 함수에 접근 가능하도록함.
@csrf_exempt
def snippet_detail(request, pk, format=None) -> JSONResponse:
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
