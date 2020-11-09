from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        print("create user")
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        return self._create_user(email, password, **extra_fields)

    def create_staff_user(self, email, password=None):
        user = self.create_user(email=email, password=password, is_staff=True)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


# Create your models here.
class User(AbstractUser):
    # nickname = models.CharField(max_length=20, blank=True, null=True)
    # profile_picture = models.ImageField(upload_to="uploaded_images", null=True, blank=True)
    # phone_number = models.CharField(max_length=11, blank=True, null=True)
    # premium = models.BooleanField(default=False)
    created = models.DateField(auto_now=True, blank=True)
    # exam_subject_combination = models.ManyToManyField(
    #     "Combination", related_name="combinations"
    # )
    profile_completed = models.BooleanField(default=False)
    # first_name = models.CharField( max_length=30, blank=True)
    # last_name = models.CharField( max_length=30, blank=True)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    email = models.EmailField(_("email address"), unique=True, null=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Article(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now= True)