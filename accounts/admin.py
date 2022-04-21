from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group


admin.site.register(get_user_model(), UserAdmin)
admin.site.unregister(Group)
# Register your models here.
