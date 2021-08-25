from django.contrib import admin
from .models import Academics, Cv, Comment
# Register your models here.

admin.site.register(Cv)
admin.site.register(Academics)

admin.site.register(Comment)