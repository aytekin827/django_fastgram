from django.contrib import admin
from .models import Image, Content

class ImageAdmin(admin.ModelAdmin):
    list_display = ('order','content')


admin.site.register(Image, ImageAdmin)


class ContentAdmin(admin.ModelAdmin):
    list_display = ('user','text')


admin.site.register(Content, ContentAdmin)
