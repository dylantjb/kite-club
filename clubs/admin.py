from django.contrib import admin

from .models import Club, User

# Register your models here.
admin.site.register(User)
admin.site.register(Club)
