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
    path("api/", api_home),
    path("api/article-list/", ArticleListView.as_view()),
    path("api/article-create/", article_create),
    path("api/article-update/<int:pk>", UpdateArticle.as_view()),
    path("api/article-detail/<int:pk>", ArticleDetailView.as_view()),
    path("api/article-delete/<int:pk>", article_delete),
    path("api/article-toggle-draft/<int:pk>", article_toggle_draft),
    path("api/comment-edit-delete/<int:pk>", CommentEditDeleteView.as_view()),
    path("api/comment-create/", CommentViewSet.as_view({'post':"create"})),
    # path("api/comment-create/", CreateComment.as_view()),
    # User based api routes
    path("api/register", registration_view),
    path("api/api-login", obtain_auth_token),
    path("api/users/", UserListView.as_view()),
    path("api/users/<int:pk>", GetUpdateDeleteUser.as_view()),
    # comments
    path("comments/", include("fluent_comments.urls")),
    # Template based article routes
    path("", ArticleList.as_view(), name="home"),
    path("<slug:slug>/", ArticleDetail.as_view(), name="none"),
    path("permission-denied", api_permission_denied, name="permission_denied"),
]
