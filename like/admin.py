from django.contrib import admin
from .models import *


class TypesAdmin(admin.ModelAdmin):
    list_display = ('type_of_material',)
    search_fields = ('type_of_material',)


class PostsAdmin(admin.ModelAdmin):
    list_display = ('uid', 'title', 'material', 'content', 'published')
    list_display_links = ('title', 'material')
    search_fields = ('title', 'material')


admin.site.register(Users)
admin.site.register(MaterialTypes, TypesAdmin)
admin.site.register(Posts, PostsAdmin)
admin.site.register(Comments)
admin.site.register(Ratings)
