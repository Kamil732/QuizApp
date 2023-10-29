from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.text import slugify

from quiz_app.images import valid_url_extension

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    DEFAULT_IMAGE_URL = 'https://s3.eu-west-2.amazonaws.com/racingleaguehub/img/avatars/default.jpg'

    username        = models.CharField(max_length=25, blank=False, null=False, unique=True)
    email           = models.EmailField(max_length=60, unique=True)
    image_url       = models.URLField(default=DEFAULT_IMAGE_URL, blank=True, null=True)
    facebook        = models.URLField(blank=True, null=True)
    website         = models.URLField(blank=True, null=True)
    description     = models.TextField(blank=True, null=True)

    date_joined     = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)

    solves          = models.PositiveIntegerField(default=0)
    slug            = models.SlugField(unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = MyUserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        self.slug = self.slug[:50]

        if self.image_url == None or not(valid_url_extension(self.image_url)):
            self.image_url = self.DEFAULT_IMAGE_URL

        return super(User, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True