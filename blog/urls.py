from django.urls import path
from .views import home, api_home, article_list, article_detail, article_create, article_update, article_delete, article_toggle_draft

urlpatterns = [
    path('', home),
    path('api/', api_home),
    path('api/article-list/', article_list),
    path('api/article-create/', article_create),
    path('api/article-update/<int:pk>', article_update),
    path('api/article-detail/<int:pk>', article_detail),
    path('api/article-delete/<int:pk>', article_delete),
    path('api/article-toggle-draft/<int:pk>', article_toggle_draft),

]