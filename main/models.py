from datetime import datetime

from django.db import models
from django.utils import timezone

from account.models import User


class Category(models.Model):
    slug = models.SlugField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categories', blank=True, null=True)
    parent = models.ForeignKey('self', related_name='children', null=True, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        if self.parent:
            return f'{self.parent} --> {self.name}'
        return self.name

    @property
    def get_children(self):
        if self.children:
            return self.children.all()
        return False

class Article(models.Model):
    title = models.CharField(max_length=255)
    desciption = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    created = models.DateField(default=timezone.now())
    location = models.CharField(default='Bishkek/Kyrgyzstan', max_length=100)

    def __str__(self):
        return self.title

    @property
    def get_image(self):
        return self.article_images.first()
    def get_all_images(self):
        return self.article_images.filter
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('article', kwargs={'pk':self.pk})

class Image(models.Model):
    image = models.ImageField(upload_to='articles')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_images')

    def __str__(self):
        return self.image.url


