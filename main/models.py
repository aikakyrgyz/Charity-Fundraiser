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
    #likes and comments
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    favorites = models.ManyToManyField(User, related_name='article_favorite', blank=True)

    class Meta:
        ordering = ['-created', ]

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

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


class Donation(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name='donations', on_delete=models.CASCADE, default=1)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    card_number = models.CharField(max_length=16)


class Petition(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    category = models.ForeignKey(Category, related_name='petitions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='petitions', on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='petitions', blank=True, null = True)
    created = models.DateField(default=timezone.now())
    goal_money = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    current_money = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    goal_signature = models.IntegerField(default=0)
    current_signature = models.IntegerField(default=0)
    fundraiser = models.BooleanField(default=False)
    # likes = models.ManyToManyField(User, related_name='petition_likes', blank=True)
    # favorites = models.ManyToManyField(User, related_name='petition_favorite', blank=True)

    def __str__(self):
        return f'{self.title}'

    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created', ]


class Comment(models.Model):
    post = models.ForeignKey(Article, related_name='article_comments', on_delete=models.CASCADE)
    # petition = models.ForeignKey(Petition, related_name='petition_comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255) #person making the comment
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date_added',)

    def __str__(self):
        return f'{self.post.title}-{self.name}'




