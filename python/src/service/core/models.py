import uuid

from django.db import models
from django.db.models.signals import pre_save

from blog.utils import unique_slug_generator, validate_media


class Article(models.Model):
    """
        Project model database table
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    short_desc = models.CharField(max_length=255, null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='articles/thumbnail/', null=True, blank=True, validators=[validate_media])
    slug = models.SlugField(null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title


class ArticleImage(models.Model):
    """
        Project Image model to create database table
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    media = models.FileField(max_length=None ,upload_to='articles/medias/', validators=[validate_media])
    project = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Article image"
        verbose_name_plural = "Article images"

    def __str__(self):
        return self.media.url

# Slug Generator
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        
pre_save.connect(slug_generator, sender=Article)