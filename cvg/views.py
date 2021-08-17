from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login

from .models import Cv, Comment
from .forms import Cvform, Commentform, UserForm

# Create your views here.
def cv_list(request):
    cvs=Cv.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context = {'cvs': cvs}
    return render(request, 'cvg/cv_list.html', context)

def cv_detail(request, pk):
    cv = get_object_or_404(Cv, pk=pk)
    context = {'cv': cv}
    return render(request, 'cvg/cv_detail.html',context)

@login_required
def cv_new(request):
    if request.method == 'POST':
        form = Cvform(request.POST)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.author=request.user
            cv.published_date=timezone.now()
            cv.save()
            return redirect('cvg:cv_detail', pk=cv.pk)
    else:
        form = Cvform()
        context = {'form':form}
    return render(request, 'cvg/cv_edit.html', context) 

@login_required
def cv_edit(request, pk):
    cv=get_object_or_404(Cv, pk=pk)
    if request.method == 'POST':
        form = Cvform(request.POST, instance=cv)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.author = request.user
            cv.published_date=timezone.now()
            cv.save()
            return redirect('cvg:cv_detail', pk=cv.pk)
    else:
        form = Cvform(instance=cv)
        context = {'form':form}
    return render(request, 'cvg/cv_edit.html', context)

@login_required
def cv_draft_list(request):
    cvs=Cv.objects.filter(published_date__isnull=True).order_by('-created_date')
    context = {'cvs':cvs}
    return render(request, 'cvg/cv_draft_list.html', context)

@login_required
def cv_publish(request, pk):
    cv=get_object_or_404(Cv, pk=pk)
    cv.published()
    return redirect('cvg:cv_detail', pk=pk)

@login_required
def add_comment_to_cv(request, pk):
    cv = get_object_or_404(Cv, pk=pk)
    if request.method == 'POST':
        form = Commentform(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.cv = cv
            comment.save()
            return redirect('cvg:cv_detail', pk=cv.pk)
    else:
        form = Commentform()
        return render(request, 'cvg/addcomment.html', {'form':form})

@login_required
def remove_comment(request, pk):
    comment=get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('cvg:cv_detail', pk=comment.cv.pk)

@login_required
def comment_approve(request, pk):
    comment=get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('cvg:cv_detail', pk=comment.cv.pk)

@login_required
def delete_cv(request, pk):
    cv = get_object_or_404(Cv, pk=pk)
    cv.delete()
    # context = {'cvs': cvs}
    return redirect('cvg:cv_list')

def signup(request):
    if request.user.is_authenticated:
        return redirect('cvg:cv_list')
    else:
        if request.method == 'POST':
            form=UserForm(request.POST)
            if form.is_valid():
                new_user=User.objects.create_user(**form.cleaned_data)
                login(request, new_user)
                return redirect('cvg:cv_list')
        else:
            form=UserForm()
        return render(request, 'cvg/signup.html', {'form': form})