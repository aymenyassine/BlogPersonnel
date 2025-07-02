from django.contrib import admin
from .models import Post,Signaler,Category

admin.site.register(Post)
admin.site.register(Signaler)
admin.site.register(Category)