from rest_framework import serializers
from .models import Article, User


class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField('get_author_name')

    class Meta:
        model = Article
        fields = ['title', 'created_by', 'modified','created','body','draft', 'author_name']

    def get_author_name(self, article):
        author_name= article.created_by.email
        return author_name





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