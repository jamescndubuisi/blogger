from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .serializers import ArticleSerializer, RegistrationSerializer, UserSerializer
from .models import Article, User
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token


# Create your views here.
def home(request):
    message = "Welcome"
    return render(request,'index.html',{"message":message})


@api_view(['GET'])
def api_home(request):
    return Response({"Message":"This is the api root directory"})


class ArticleListView(ListAPIView):
    queryset = Article.objects.filter(draft=False).order_by('created')
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("title","created_by__email","body")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def article_detail(request,pk):
    article = get_object_or_404(Article,id=pk,draft=False)
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_create(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_update(request,pk):
    article = get_object_or_404(Article,id=pk,draft=False)
    print(request.data)
    serializer = ArticleSerializer(instance=article,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def article_toggle_draft(request,pk):
    article = get_object_or_404(Article,id=pk,draft=False)
    return Response({"message":"Nothing Happened"})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def article_delete(request,pk):
    article = get_object_or_404(Article,id=pk,draft=False)
    article.delete()
    return Response({"message" : f"object with id {pk} , was deleted successfully"})


@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user).key
        data['token'] = token
        data['email'] = user.email
        data['message'] = "User created"
    else:
        data['message'] = serializer.errors
    return Response(data)



class UserListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = [TokenAuthentication, ]
    queryset = User.objects.all()


class GetUpdateDeleteUser(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = [TokenAuthentication, ]
    queryset = User.objects.all()



