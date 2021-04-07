from django.contrib import admin

from main.models import *

class ImageInlineAdmin(admin.TabularInline):
    model = Image
    fields = ('image',)
    max_num = 5

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ImageInlineAdmin,]
admin.site.register(Category)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'date_added',)
    list_filter = ('date_added', 'date_updated')
    search_fields = ('name', 'body')


