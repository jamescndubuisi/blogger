from django.urls import path, include
from .views import (
    api_home,
    ArticleListView,
    # article_detail,
    article_create,
    article_update,
    article_delete,
    article_toggle_draft,
    registration_view,
    UserListView,
    GetUpdateDeleteUser,
    ArticleList,
    ArticleDetail,
    ArticleDetailView,
)

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("api/", api_home),
    path("api/article-list/", ArticleListView.as_view()),
    path("api/article-create/", article_create),
    path("api/article-update/<int:pk>", article_update),
    path("api/article-detail/<int:pk>", ArticleDetailView.as_view()),
    path("api/article-delete/<int:pk>", article_delete),
    path("api/article-toggle-draft/<int:pk>", article_toggle_draft),
    path("api/register", registration_view),
    path("api/api-login", obtain_auth_token),
    path("api/users/", UserListView.as_view()),
    path("api/users/<int:pk>", GetUpdateDeleteUser.as_view()),
    path('comments/', include('fluent_comments.urls')),
    # Template based url
    path("", ArticleList.as_view(), name = "home"),
    path("<slug:slug>/", ArticleDetail.as_view(), name = "home"),
]
