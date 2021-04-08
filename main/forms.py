from django import forms
from .models import Article, Image, Comment, Donation, Petition

class PostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'desciption', 'user', 'created', 'location', 'category' )

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('name', 'amount', 'card_number',)

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ('title', 'body', 'category', 'image', 'goal_money', 'goal_signature')
