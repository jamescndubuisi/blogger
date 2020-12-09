from django.urls import path, include


# from rest_framework import routers
# from .views import CommentViewSet
#
# router.register(r'poll',PollViewSet)
# router.register(r'comment',CommentViewSet)

from .views import (
    api_home,
    ArticleListView,
    CommentEditDeleteView,
    article_create,
    # article_update,
    UpdateArticle,
    article_delete,
    article_toggle_draft,
    registration_view,
    UserListView,
    GetUpdateDeleteUser,
    ArticleList,
    ArticleDetail,
    ArticleDetailView,
    CreateComment,
    CommentViewSet,
api_permission_denied,
)

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Article based Api routes
    path("api/", api_home, name='api_home'),
    path("api/article-list/", ArticleListView.as_view(),name='article-list'),
    path("api/article-create/", article_create,name='create-article'),
    path("api/article-update/<int:pk>", UpdateArticle.as_view(),name='update-article'),
    path("api/article-detail/<int:pk>", ArticleDetailView.as_view(),name='api-article-detail'),
    path("api/article-delete/<int:pk>", article_delete,name="delete-article"),
    path("api/comment-edit-delete/<int:pk>", CommentEditDeleteView.as_view(),name='edit-delete-comment'),
    path("api/comment-create/", CommentViewSet.as_view({'post':"create"}),name='create-comment'),
    # path("api/comment-create/", CreateComment.as_view()),
    # User based api routes
    path("api/register", registration_view,name='api-register'),
    path("api/api-login", obtain_auth_token,name='api-login'),
    path("api/users/", UserListView.as_view(),name='api-list-users'),
    path("api/users/<int:pk>", GetUpdateDeleteUser.as_view(),name='api-view-user'),
    # comments
    path("comments/", include("fluent_comments.urls")),
    # Template based article routes
    path("", ArticleList.as_view(), name="home"),
    path("<slug:slug>/", ArticleDetail.as_view(), name="article-detail"),
    path("permission-denied", api_permission_denied, name="permission_denied"),
]
