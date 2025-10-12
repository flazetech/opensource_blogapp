from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm


def index(request):
    return render (request,'index.html')


def aboutus(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

# this is a function which will register user
def signup(request):
    if request.method == 'POST':
        # taking data form request
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # creating and saving a user instance
        try :
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()

            # logging in the user
            user = authenticate(request, username = username , password = password)
            if user is not None:
                login(request,user)

            # redirecting with message
                messages.add_message(request, messages.SUCCESS, "User Created Sucessfully!")
                return redirect('/')
            else:
                messages.add_message(request, messages.WARNING, "Some Error Occured!") 
                return redirect('signup')

        except IntegrityError:
            messages.add_message(request, messages.WARNING,'Credentials Already Taken!')
            return redirect('signup')
    else:
        return render(request,'signup.html')

    

# this is a function which will signin user
def signin(request):
    if request.method == 'POST':
        # taking data from request
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('landing_page')
        else:
            messages.add_message(request, messages.ERROR, "Invalid Credentials!")
            return redirect('signin')
    else:
        return render(request,'signin.html')
    

def blog_list(request):
    posts = Post.objects.filter(is_published=True).select_related("author")
    return render(request, "blog/list.html", {"posts": posts})

def blog_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related("author"), slug=slug, is_published=True)
    cform = CommentForm()
    return render(request, "blog/detail.html", {"post": post, "cform": cform})

@login_required
def blog_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post published!")
            return redirect("blog_detail", slug=post.slug)
    else:
        form = PostForm()
    return render(request, "blog/form.html", {"form": form, "mode": "create"})

@login_required
def blog_edit(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated.")
            return redirect("blog_detail", slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/form.html", {"form": form, "mode": "edit", "post": post})

@login_required
def blog_delete(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect("blog_list")
    return render(request, "blog/confirm_delete.html", {"post": post})

@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(post=post, author=request.user, content=form.cleaned_data["content"])
            messages.success(request, "Comment added.")
    return redirect("blog_detail", slug=post.slug)

@login_required
def toggle_like(request, slug):
    # quick AJAX/POST like toggle
    post = get_object_or_404(Post, slug=slug, is_published=True)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"liked": liked, "count": post.likes_count})
    return redirect("blog_detail", slug=post.slug)

