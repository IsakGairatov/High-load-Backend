from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import PostForm, RegisterUserForm, CommentForm
from .models import Post
# Create your views here.

def showPosts(request):
    Posts = Post.objects.all()
    paginator = Paginator(Posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'blogapp/posts.html', {"Posts": page_obj})

def showPost(request, id):
    Post0 = Post.objects.get(id=id)

    if request.method == 'POST':
        comform = CommentForm(request.POST)
        if comform.is_valid():
            comform.instance.author = request.user
            comform.instance.post = Post0
            c = comform.save()
            return redirect(f'Posts')
    else:
        comform = CommentForm()
    comments = Post0.comment_set.all()

    return render(request, 'blogapp/post.html', {'Post': Post0, 'form': comform, 'comments': comments})

def makePost(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            post_form.instance.author = request.user
            p = post_form.save()
            return redirect(f'Posts')
    else:
        post_form = PostForm()

    return render(request, 'blogapp/makepost.html', {'post_form': post_form, 'Title': 'Создание поста'})

def delPost(request, id):
    p = Post.objects.get(id=id)
    if p.author != request.user:
        redirect('Posts')
    else:
        p.delete()
        return redirect('Posts')

def updatePost(request, id):
    p = Post.objects.get(id=id)
    if p.author != request.user:
        redirect('Posts')
    else:

        if request.method == 'POST':
            post_form = PostForm(request.POST, instance=p)

            if post_form.is_valid():
                post_form.save()
                return redirect('postpage', id=p.id)
        else:
            post_form = PostForm(instance=p)

        return render(request, 'blogapp/makepost.html', {'post_form': post_form, 'Title': 'Изменение поста'})



class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'blogapp/login.html'
    extra_context = {'Title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('Posts')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'blogapp/login.html'
    success_url = reverse_lazy('login')
    extra_context = {'Title': 'Регистрация'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('Posts')



def logout_user(request):
    logout(request)
    return redirect('login')

