from django import forms
from .models import Article, Image, Comment, Donation, Petition
from account.models import Signer


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


class SignForm(forms.ModelForm):
    class Meta:
        model = Signer
        fields = ('first_name', 'last_name', 'location',)


class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ('title', 'body', 'category', 'image', 'fundraiser', 'goal_money', 'goal_signature', )


