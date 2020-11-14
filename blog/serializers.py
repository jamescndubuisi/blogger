from rest_framework import serializers
from .models import Article, User
from fluent_comments.models import get_comments_model, FluentComment

class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField('get_author_name')

    class Meta:
        model = Article
        fields = ['title', 'created_by', 'modified','created','body','draft', 'author_name']

    def get_author_name(self, article):
        author_name= article.created_by.email
        return author_name



class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = FluentComment
        fields = "__all__"


class ArticleDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField("get_comments")
    author_name = serializers.SerializerMethodField("get_author_name")
    class Meta:
        model = Article
        # fields = '__all__'
        fields = ['title', 'created_by', 'modified','created','body','draft', 'author_name','comments']

    def get_author_name(self, article):
        author_name= article.created_by.email
        return author_name


    def get_comments(self, article):
        comment= FluentComment.objects.filter(object_pk=article.id)
        serializer = CommentSerializer(comment, many=True)
        return serializer.data





class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self, **kwargs):
        user = User(email=self.validated_data["email"])
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"password": "passwords must match"})
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'pk','first_name','last_name']