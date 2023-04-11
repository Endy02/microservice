from django.contrib import admin

from core.models import Article, ArticleImage


class ArticleImageAdmin(admin.StackedInline):
    model = ArticleImage
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleImageAdmin,]
    search_fields = ('created_at',)
    list_filter = ('created_at',)
    list_display = ('id', 'title', 'slug', 'created_at', 'updated_at')
    ordering = ("-created_at",)
    fieldsets = (
        (None, {'fields': ('title', 'description', 'short_desc')}),
        ('General', {'fields': ('link', 'thumbnail', 'slug')})        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('title', 'description', 'short_desc', 'link', 'thumbnail', 'slug')}
         ),
    )