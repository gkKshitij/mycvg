from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login

from .models import Student, Comment
from .forms import Studentform, Commentform, UserForm

# Create your views here.
def student_list(request):
    students=Student.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context = {'students': students}
    return render(request, 'cvg/student_list.html', context)

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    context = {'student': student}
    return render(request, 'cvg/student_detail.html',context)

@login_required
def student_new(request):
    if request.method == 'POST':
        form = Studentform(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.author=request.user
            student.published_date=timezone.now()
            student.save()
            return redirect('cvg:student_detail', pk=student.pk)
    else:
        form = Studentform()
        context = {'form':form}
    return render(request, 'cvg/student_edit.html', context) 

@login_required
def student_edit(request, pk):
    student=get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = Studentform(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.author = request.user
            student.published_date=timezone.now()
            student.save()
            return redirect('cvg:student_detail', pk=student.pk)
    else:
        form = Studentform(instance=student)
        context = {'form':form}
    return render(request, 'cvg/student_edit.html', context)

@login_required
def student_draft_list(request):
    students=Student.objects.filter(published_date__isnull=True).order_by('-created_date')
    context = {'students':students}
    return render(request, 'cvg/student_draft_list.html', context)

@login_required
def student_publish(request, pk):
    student=get_object_or_404(Student, pk=pk)
    student.published()
    return redirect('cvg:student_detail', pk=pk)

@login_required
def add_comment_to_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = Commentform(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.student = student
            comment.save()
            return redirect('cvg:student_detail', pk=student.pk)
    else:
        form = Commentform()
        return render(request, 'cvg/addcomment.html', {'form':form})

@login_required
def remove_comment(request, pk):
    comment=get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('cvg:student_detail', pk=comment.student.pk)

@login_required
def comment_approve(request, pk):
    comment=get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('cvg:student_detail', pk=comment.student.pk)

@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    # context = {'students': students}
    return redirect('cvg:student_list')

def signup(request):
    if request.user.is_authenticated:
        return redirect('cvg:student_list')
    else:
        if request.method == 'POST':
            form=UserForm(request.POST)
            if form.is_valid():
                new_user=User.objects.create_user(**form.cleaned_data)
                login(request, new_user)
                return redirect('cvg:student_list')
        else:
            form=UserForm()
        return render(request, 'cvg/signup.html', {'form': form})