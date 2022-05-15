import email
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime

# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, is_active, **kwargs):
        if not email:
            raise ValueError('Email require')
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            is_active = is_active,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, **kwargs):
        return self._create_user(email, password, False, False, False, **kwargs)
    
    def create_superuser(self, email, password, **kwargs):
        return self._create_user(email, password, True, True, True, **kwargs)
    
    
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=100, unique=True)
    banned = models.IntegerField(default=0)
    ban_reason = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(default=datetime.now)
    modified = models.DateTimeField(default=datetime.now)
    last_login = models.DateTimeField(default=datetime.now)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=10)
    notification = models.IntegerField(default=0)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    class Meta:
        managed = False
        db_table = "users"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def user_active(self):
        return self.is_active

    def profile(self):
        return {
                "id": self.id,
                "firstname": self.first_name,
                "lastname": self.last_name,
                "email": self.email,
                "language": self.language
                }
