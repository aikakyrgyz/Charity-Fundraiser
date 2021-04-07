from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from .forms import ImageForm
from .permissions import *
from main.models import *
from .forms import PostForm


# def index(request):
#     articles = Article.objects.all()
#     return render(request, 'index.html', {'articles':articles})

class MainPageView(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'articles'

    def get_template_names(self):
        template_name = super(MainPageView, self).get_template_names()
        search = self.request.GET.get('q')
        if search:
            template_name = 'search.html'
        return template_name

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('q')
        if search:
            context['articles'] = Article.objects.filter(Q(title__icontains=search)|
                                                         Q(desciption__icontains=search))
        else:
            context['articles'] = Article.objects.all()
        return context
#
# def category_detail(request, slug):
#     category = Category.objects.get(slug=slug)
#     articles = Article.objects.filter(category_id=slug)
#     return render(request, 'blog.html', locals())

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog.html'
    context_object_name = 'category'
    paginate_by = 1

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.slug = kwargs.get('slug', None)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(category_id=self.slug)
        return context

# def article_detail(request, pk):
#     article = get_object_or_404(Article, pk=pk)
#     image = article.get_image
#     images = article.article_images.exclude(id = image.id)
#     return render(request, 'blog-single.html', locals())

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog-single.html'
    context_object_name = 'article'
    def get_context_data(self, **kwargs):
        context = super(). get_context_data(**kwargs)
        image = self.get_object().get_image
        context['images'] = self.get_object().article_images.exclude(id=image.id)
        return context

@login_required(login_url='login')
def create_post(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if post_form.is_valid() and formset.is_valid():
            post = post_form.save()
            for form in formset.cleaned_data:
                image = form['image']
                Image.objects.create(image=image, article=post)
            return redirect(post.get_absolute_url())
    else:
        post_form = PostForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'create_post.html', locals())



def update_post(request, pk):
    post = get_object_or_404(Article, pk=pk)
    if request.user == post.user:

        ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
        post_form = PostForm(request.POST or None, instance = post)
        formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.filter(article=post))
        if post_form.is_valid() and formset.is_valid():
            post = post_form.save()
            for form in formset:
                image = form.save(commit=False)
                image.article = post
                image.save()
            return redirect(post.get_absolute_url())
        return render(request, 'update_post.html', locals())
    else:
        return HttpResponse('Forbidden')

# def delete_post(request, pk):
#     post = get_object_or_404(Article, pk=pk)
#     category = post.category.slug
#     if request.method == 'POST':
#         post.delete()
#         messages.add_message(request, messages.SUCCESS, 'Successfully deleted')
#         return redirect('category', slug=category)
#     return render(request, 'delete_post.html')

class DeleteArticleView(UserHasPermissionMixin, DeleteView):
    model = Article
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.add_message(request, messages.SUCCESS, 'Successfully deleted!')
        return HttpResponseRedirect(success_url)
