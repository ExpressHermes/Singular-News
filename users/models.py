from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
# from django.contrib.postgres.fields import ArrayField


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)


class UserInterest(models.Model):
    user = models.ForeignKey(User, related_name='user',
                             verbose_name='user', on_delete=models.CASCADE)
    interests = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.user)


class UserFeedback(models.Model):
    BOOL_CHOICES = [
        (True, 'Yes'), (False, 'No')
    ]
    SATISFACTION_CHOICES = [
        ('5', 'Very Satisfield'),
        ('4', 'Satisfied'),
        ('3', 'Neutral'),
        ('2', 'Unsatisfied'),
        ('1', 'Very unsatisfied'),
    ]
    SITE_RETURN_CHOICES = [
        ('5', 'Very Likely'),
        ('4', 'Likely'),
        ('3', 'Sometimes'),
        ('2', 'Not Likely'),
        ('1', 'Never'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    first_visit = models.BooleanField(max_length=1, choices=BOOL_CHOICES)
    satisfaction = models.CharField(max_length=1, choices=SATISFACTION_CHOICES)
    site_return = models.CharField(max_length=1, choices=SITE_RETURN_CHOICES)
    article_num = models.IntegerField()
    suggestion = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserBookmark(models.Model):
    User = models.ForeignKey(
        User, related_name='user_bookmarks', on_delete=models.CASCADE)
    bookmarks = ArrayField(models.CharField(
        max_length=30), size=10, blank=True, null=True)

    def __str__(self):
        return str(self.User)
