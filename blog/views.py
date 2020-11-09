from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ArticleSerializer
from .models import Article
from rest_framework.viewsets import GenericViewSet


# Create your views here.
def home(request):
    message = "Welcome"
    return render(request,'index.html',{"message":message})

@api_view(['GET'])
def api_home(request):
    return Response({"Message":"This is the api root directory"})

@api_view(['GET'])
def article_list(request):
    articles = Article.objects.filter(draft=False)
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def article_detail(request,pk):
    article = get_object_or_404(Article,id=pk,draft=False)
    # article = Article.objects.get(id=pk, draft=False)
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def article_create(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def article_update(request,pk):
    article = get_object_or_404(Article,id=pk,draft=False)
    print(request.data)
    serializer = ArticleSerializer(instance=article,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



@api_view(['GET'])
def article_toggle_draft(request,pk):
    article = get_object_or_404(Article,id=pk,draft=False)


    return Response({"message":"Nothing Happened"})



@api_view(['DELETE'])
def article_delete(request,pk):
    article = get_object_or_404(Article,id=pk,draft=False)
    article.delete()
    return Response({"message":f"object with id {pk} , was deleted successfully"})