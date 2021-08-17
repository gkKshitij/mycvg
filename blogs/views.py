from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login

from .models import Post, Comment
from .forms import Postform, Commentform, UserForm

# Create your views here.
def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context = {'posts': posts}
    return render(request, 'blogs/post_list.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {'post': post}
    return render(request, 'blogs/post_detail.html',context)

@login_required
def post_new(request):
    if request.method == 'POST':
        form = Postform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author=request.user
            post.published_date=timezone.now()
            post.save()
            return redirect('blogs:post_detail', pk=post.pk)
    else:
        form = Postform()
        context = {'form':form}
    return render(request, 'blogs/post_edit.html', context) 

@login_required
def post_edit(request, pk):
    post=get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = Postform(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date=timezone.now()
            post.save()
            return redirect('blogs:post_detail', pk=post.pk)
    else:
        form = Postform(instance=post)
        context = {'form':form}
    return render(request, 'blogs/post_edit.html', context)

@login_required
def post_draft_list(request):
    posts=Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    context = {'posts':posts}
    return render(request, 'blogs/post_draft_list.html', context)

@login_required
def post_publish(request, pk):
    post=get_object_or_404(Post, pk=pk)
    post.published()
    return redirect('blogs:post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = Commentform(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blogs:post_detail', pk=post.pk)
    else:
        form = Commentform()
        return render(request, 'blogs/addcomment.html', {'form':form})

@login_required
def remove_comment(request, pk):
    comment=get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blogs:post_detail', pk=comment.post.pk)

@login_required
def comment_approve(request, pk):
    comment=get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blogs:post_detail', pk=comment.post.pk)

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    # context = {'posts': posts}
    return redirect('blogs:post_list')

def signup(request):
    if request.user.is_authenticated:
        return redirect('blogs:post_list')
    else:
        if request.method == 'POST':
            form=UserForm(request.POST)
            if form.is_valid():
                new_user=User.objects.create_user(**form.cleaned_data)
                login(request, new_user)
                return redirect('blogs:post_list')
        else:
            form=UserForm()
        return render(request, 'blogs/signup.html', {'form': form})