from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView

from .forms import PostForm, RegisterUserForm, CommentForm, UpdateUserForm, UserDataForm, TagForm
from .models import Post, UserData, TagRelationship, Tag


# Create your views here.

@cache_page(60 * 1)
def showPosts(request):
    Posts = Post.objects.prefetch_related('comments').prefetch_related('tagrelationship_set')

    paginator = Paginator(Posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'blogapp/posts.html', {"Posts": page_obj})

def showTagPosts(request, tag_id):
    Posts = TagRelationship.objects.filter(tag__id=tag_id).prefetch_related('comments').prefetch_related('tagrelationship_set')
    Posts = [p.post for p in Posts]
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
    comments = Post0.comments.all()

    return render(request, 'blogapp/post.html', {'Post': Post0, 'form': comform, 'comments': comments})

def makePost(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            post_form.instance.author = request.user
            p = post_form.save()
            return redirect('editPost', id=p.id)

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

def editPost(request, id):
    p = Post.objects.get(id=id)
    if p.author != request.user:
        redirect('Posts')
    else:

        if request.method == 'POST':
            post_form = PostForm(request.POST, instance=p)
            tag_form = TagForm(request.POST)

            if post_form.is_valid():
                post_form.save()
                return redirect('postpage', id=p.id)
            if tag_form.is_valid():
                tag_form.instance.post = p
                tag_form.save()
                return redirect(request.META['HTTP_REFERER'])

        else:
            post_form = PostForm(instance=p)
            tag_form = TagForm()

        return render(request, 'blogapp/editpost.html', {'post_form': post_form, 'tag_form': tag_form, 'p': p, 'Title': 'Изменение поста'})

def deltag(request, post, tag):
    TagRelationship.objects.get(post__id=post, tag__id=tag).delete()
    return redirect(request.META['HTTP_REFERER'])


def Profile(request):
    if request.user.is_authenticated:
        Posts = Post.objects.filter(author=request.user).prefetch_related('comments').prefetch_related('tagrelationship_set')
        Pnum = cache.get(f'amount of posts {Posts[0].author}')

        if Pnum == None:
            Pnum = Posts.count()
            cache.set(f'amount of posts {Posts[0].author}', Pnum, 500)

        paginator = Paginator(Posts, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, 'blogapp/profile.html', {'user': request.user, 'pnum': Pnum, 'Posts': page_obj})
    else:
        return redirect('login')

def ProfileEdit(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            f1= UpdateUserForm(request.POST, instance=request.user)
            f2 = UserDataForm(request.POST, instance=request.user.userdata)

            if f1.is_valid() and f2.is_valid():
                f1.save()
                f2.save()
                return redirect('Profile')
        else:
            f1 = UpdateUserForm(instance=request.user)
            f2 = UserDataForm(instance=request.user.userdata)
        return render(request, 'blogapp/profileedit.html', {'Title': 'Редактирование профиля', 'form1': f1, 'form2': f2})
    else:
        return redirect('login')

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
        UserData.objects.create(user=form.instance, bio='Пока ничего нету')
        login(self.request, user)

        return redirect('Posts')



def logout_user(request):
    logout(request)
    return redirect('login')

