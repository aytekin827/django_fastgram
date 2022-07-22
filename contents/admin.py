from django.contrib import admin
from .models import Image, Content


class ImageInline(admin.TabularInline):
    model = Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ('order','content')
admin.site.register(Image, ImageAdmin)


class ContentAdmin(admin.ModelAdmin):
    list_display = ('user','text','created_at')
    inlines = [ImageInline] # 동일한 페이지에서 image모델과 content모델 둘다 볼 수 있다.

admin.site.register(Content, ContentAdmin)
