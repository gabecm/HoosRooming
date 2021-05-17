from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import User, Message


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username']}),
        (None, {'fields': ['first_name']}),
        (None, {'fields': ['last_name']}),
        (None, {'fields': ['email']}),
        (None, {'fields': ['phone_number']}),
        (None, {'fields': ['bio']}),
        (None, {'fields': ['cleanliness_level']}),
        (None, {'fields': ['noise_level']}),
        (None, {'fields': ['morning_preference']}),
        (None, {'fields': ['lease']}),
        (None, {'fields': ['budget']}),
        (None, {'fields': ['image']}),
        (None, {'fields': ['spotify_song']}),
        (None, {'fields': ['spotify_artist']}),
        (None, {'fields': ['spotify_link']}),
    ]
    list_display = ('first_name', 'username', 'email', 'phone_number')


class MessageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'sender', 'receiver', 'msg_content']})
    ]
    list_display = ('user', 'sender', 'receiver', 'msg_content')
    search_fields = ['user']


admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)