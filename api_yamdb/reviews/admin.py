from django.contrib import admin

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'score', 'author', 'title', 'pub_date')
    search_fields = ('text',)
    list_filter = ('text',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'review', 'pub_date')
    search_fields = ('text',)
    list_filter = ('text',)
    empty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre)
admin.site.register(GenreTitle)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title)
