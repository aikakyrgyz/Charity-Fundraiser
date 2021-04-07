from django import forms
from .models import Article, Image

class PostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', )
