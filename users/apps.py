from django.apps import AppConfig
from django.contrib import admin
from users.models import UserAccountInfo


class UsersConfig(AppConfig):
    name = 'users'


admin.site.register(UserAccountInfo)
