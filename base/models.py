from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, is_active, **kwargs):
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            is_staff = is_staff,
            is_active = is_active,
            is_superuser = is_superuser,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, **kwargs):
        return self._create_user(email, password, False, False, False, **kwargs)
    
    def create_superuser(self, email, password, **kwargs):
        user = self._create_user(email, password, True, True, True, **kwargs)
        

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=100, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    banned = models.IntegerField(default=0)
    ban_reason = models.CharField(max_length=255, blank=True, null=True)
    last_login = models.DateTimeField(default=datetime.now)
    created = models.DateTimeField(default=datetime.now)
    modified = models.DateTimeField(default=datetime.now)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=10)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    class Meta:
        db_table = "users"
    
    
class Dashboard(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    iframe = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    active = models.IntegerField(default=1)
    users = models.ManyToManyField(User, related_name='dashboards')
    class Meta:
        managed = False
        db_table = "dashboards"
        

class Languages(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, default=datetime.now)

    class Meta:
        managed = False
        db_table = "languages"
        verbose_name_plural = "Languages"

    def __str__(self):
        return self.name