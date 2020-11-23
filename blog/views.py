from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .serializers import ArticleSerializer, RegistrationSerializer, UserSerializer, CommentSerializer, ArticleDetailSerializer, NormalCommentSerializer
from .models import Article, User
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from django.views import generic
from fluent_comments.models import FluentComment
from rest_framework import viewsets
from django.contrib.contenttypes.models import ContentType
import datetime
from blogger import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import UserPassesTestMixin


def user_is_owner(func):

    def check_and_call(request,*args,**kwargs):
        pk=kwargs['pk']
        article = Article.objects.get(pk)
        if not (article.user.id==request.user.id):
            return Response(status=403,data={'message':"you are not the rightful owner"}, content_type="application/json")
        return func(request,*args,**kwargs)
    return check_and_call


# Create your views here.
class ArticleList(generic.ListView):
    template_name = "index.html"
    context_object_name = "articles"
    queryset = Article.objects.all()

class ArticleDetail(generic.DetailView):
    template_name = "articledetail.html"
    context_object_name = "article"
    model = Article
    slug_field = "slug"


@api_view(['GET'])
def api_home(request):
    return Response({"Message":"This is the api root directory"})


class CreateComment(CreateAPIView):
    model = FluentComment
    serializer_class = NormalCommentSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination



class ArticleListView(ListAPIView):
    queryset = Article.objects.filter(draft=False).order_by('created')
    serializer_class = ArticleSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("title","created_by__email","body")

class ArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    pagination_class = PageNumberPagination



class CommentEditDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = FluentComment.objects.all()
    serializer_class = NormalCommentSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_create(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# # @user_is_owner
# def article_update(request,pk):
#     article = get_object_or_404(Article,id=pk,draft=False)
#     print(request.data)
#     serializer = ArticleSerializer(instance=article,data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)


class UpdateArticle(UserPassesTestMixin,RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination
    login_url = "permission_denied"

    def test_func(self):
        article = Article.objects.get(pk = self.kwargs.get("pk"))
        return self.request.user is article.created_by




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



class CommentViewSet(viewsets.ModelViewSet):
    queryset = FluentComment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CommentViewSet,self).dispatch(request,*args, **kwargs)

    # @csrf_exempt
    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data = self.request.data
            comment = data['comment']
            poll = data['object_pk']
            if 'parent' in data:
                parent = data['parent']
            else:
                parent = None
            submit_date = datetime.datetime.now()
            content = ContentType.objects.get(model="Article").pk
            comment = FluentComment.objects.create(object_pk=poll,comment=comment, submit_date=submit_date,   content_type_id=content,user_id = self.request.user.id,site_id=settings.SITE_ID, parent_id=parent)
            serializer = CommentSerializer(comment,context=  {'request': request})
            return Response(serializer.data)



## Error Pages
def server_error(request):
    data = request.path
    return render(request, "errors/500.html", {"data": data})


def not_found(request, exception):
    data = request.path
    print(data)
    return render(request, "errors/404.html", {"data": data})


def permission_denied(request, exception):
    data = request.path
    return render(request, "errors/403.html", {"data": data})

@api_view(['GET'])
def api_permission_denied(request):
    data = request.path
    return Response(status=403, data={"message":"Permission denied"})


def bad_request(request, exception):
    data = request.path
    return render(request, "errors/400.html", {"data": data})
