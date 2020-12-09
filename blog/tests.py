from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from .views import (
api_home,
ArticleListView,
article_create,
UpdateArticle,
ArticleDetail,
article_delete,
CommentEditDeleteView,
CommentViewSet,
registration_view,
UserListView,
GetUpdateDeleteUser,
ArticleList,
ArticleDetailView,
CreateComment,
)

# Create your tests here.


class TestUrls(SimpleTestCase):
    print("Url Test")

    def setUp(self):
        pass

    def test_api_home_is_resolved(self):
        url = reverse("api_home")
        self.assertEquals(resolve(url).func, api_home)

    def test_api_list_article_is_resolved(self):
        url = reverse("article-list")
        self.assertEquals(resolve(url).func.view_class, ArticleListView)

    def test_api_create_article_is_resolved(self):
        url = reverse("create-article")
        self.assertEquals(resolve(url).func, article_create)

    def test_api_update_article_is_resolved(self):
        url = reverse("update-article",args=[1])
        self.assertEquals(resolve(url).func.view_class, UpdateArticle)


    def test_api_detail_article_is_resolved(self):
        url = reverse("api-article-detail", args=[1])
        self.assertEquals(resolve(url).func.view_class, ArticleDetailView)


    def test_api_delete_article_is_resolved(self):
        url = reverse("delete-article",args=[1])
        self.assertEquals(resolve(url).func, article_delete)


    def test_api_view_article_comments_edit_delete_is_resolved(self):
        url = reverse("edit-delete-comment", args=[1])
        self.assertEquals(resolve(url).func.view_class, CommentEditDeleteView)

    # def test_api_view_article_comments_create_is_resolved(self):
    #     url = reverse("create-comment",args=['create'])
    #     view = CommentViewSet.as_view({'post':"create"})
    #     self.assertEquals(resolve(url).func, view)


    def test_api_register_is_resolved(self):
        url = reverse("api-register")
        self.assertEquals(resolve(url).func, registration_view)

    def test_api_users_is_resolved(self):
        url = reverse("api-list-users")
        self.assertEquals(resolve(url).func.view_class, UserListView)

    def test_api_view_user_is_resolved(self):
        url = reverse("api-view-user",args=[1])
        self.assertEquals(resolve(url).func.view_class, GetUpdateDeleteUser)

    def test_article_detail_is_resolved(self):
        url = reverse("article-detail", args=[1])
        self.assertEquals(resolve(url).func.view_class, ArticleDetail)


class TestViews(SimpleTestCase):
    print("View Test")
    pass


class TestModels(TestCase):
    print("Model Test")
    pass


class TestForms(SimpleTestCase):
    print("Form Test")
    pass


class TestSerializers(SimpleTestCase):
    print("Serializer Test")
    pass
