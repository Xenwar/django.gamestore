from .models import Member,ActivationData

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class MemberAdmin(admin.ModelAdmin):
    pass#fields = ('first_name','last_name','email',)

admin.site.register(Member, UserAdmin)


@admin.register(ActivationData)
class ActivationDataAdmin(admin.ModelAdmin):
    pass#fields = ('first_name','last_name','email', 'player_games')