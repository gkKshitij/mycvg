from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Academics, Cv, Comment
from .forms import Cvform, Commentform, UserForm, Academicsform


# Create your views here.

# unused functions from last app
@login_required
def cv_draft_list(request):
    cvs = Cv.objects.filter(published_date__isnull=True).order_by('-created_date')
    context = {'cvs': cvs}
    return render(request, 'cvg/cv_draft_list.html', context)


@login_required
def cv_publish(request, pk):
    cv = get_object_or_404(Cv, pk=pk)
    cv.published()
    return redirect('cvg:cv_detail', pk=pk)


# signup custom view
def signup(request):
    if request.user.is_authenticated:
        return redirect('cvg:cv_list')
    else:
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                new_user = User.objects.create_user(**form.cleaned_data)
                login(request, new_user)
                return redirect('cvg:cv_list')
        else:
            form = UserForm()
        return render(request, 'cvg/signup.html', {'form': form})


# Home
def cv_list(request):
    cvs = Cv.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context = {'cvs': cvs}
    return render(request, 'cvg/cv_list.html', context)


# s1-step1 takes to details of cv
def cv_detail(request, pk):
    cv = get_object_or_404(Cv, pk=pk)
    context = {'cv': cv}
    return render(request, 'cvg/cv_detail.html', context)


# views related to cv-basic details
@login_required
def cv_new(request):
    if request.method == 'POST':
        form = Cvform(request.POST)
        if form.is_valid():
            try:
                cvd = form.save(commit=False)
                cvd.sap_id = int(str(request.user))
                cvd.created_by = request.user
                cvd.published_date = timezone.now()
                cvd.save()
                return redirect('cvg:cv_detail', pk=cvd.pk)
            except:
                return HttpResponse("Please maintain only one Cv")
                # TODO: make this later          
    else:
        form = Cvform()
    return render(request, 'cvg/cv_edit.html', {'form': form})


@login_required
def delete_cv(request, pk):
    cv = get_object_or_404(Cv, pk=pk)
    cv.delete()
    # context = {'cvs': cvs}
    return redirect('cvg:cv_list')


## generic form of above view
# class Cv_new(LoginRequiredMixin, CreateView):
#     # fields = '__all__'
#     model = Cv
#     form_class = Cvform
#     template_name = 'cvg/cv_edit.html'
#     def form_valid(self, form):
#         form.instance.created_by=self.request.user
#         return super().form_valid(form)

# edit cv basic details
@login_required
def cv_edit(request, pk):
    cv = get_object_or_404(Cv, pk=pk)
    if request.method == 'POST':
        form = Cvform(request.POST, instance=cv)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.edited_by = str(request.user)
            cv.published_date = timezone.now()
            cv.save()
            return redirect('cvg:cv_detail', pk=cv.pk)
    else:
        form = Cvform(instance=cv)
        context = {'form': form}
    return render(request, 'cvg/cv_edit.html', context)


## generic form of above view
# class Cv_edit(LoginRequiredMixin, UpdateView):
#     # fields = '__all__'
#     model = Cv
#     form_class = Cvform
#     template_name = 'cvg/cv_edit.html'
#     def form_valid(self, form):
#         form.instance.created_by=self.request.user
#         return super().form_valid(form)


# ad=academic details and views related to that
@login_required
def add_ad_to_cv(request, pk):
    cv = get_object_or_404(Cv, pk=pk)
    if request.method == 'POST':
        adform = Academicsform(request.POST)
        if adform.is_valid():
            ad = adform.save(commit=False)
            ad.cv = cv
            ad.save()
            return redirect('cvg:cv_detail', pk=cv.pk)
    else:
        adform = Academicsform()
    return render(request, 'cvg/add_ad.html', {'adform': adform})


@login_required
def edit_ad(request, pk):
    ad = get_object_or_404(Academics, pk=pk)
    if request.method == 'POST':
        adform = Academicsform(request.POST, instance=ad)
        if adform.is_valid():
            ad = adform.save(commit=False)
            ad.save()
            return redirect('cvg:cv_detail', pk=ad.cv.pk)
    else:
        adform = Academicsform(instance=ad)
    return render(request, 'cvg/add_ad.html', {'adform': adform})


@login_required
def remove_ad(request, pk):
    ad = get_object_or_404(Academics, pk=pk)
    ad.delete()
    return redirect('cvg:cv_detail', pk=ad.cv.pk)


@login_required
def unapprove_ad(request, pk):
    ad = get_object_or_404(Academics, pk=pk)
    ad.unapprove()
    return redirect('cvg:cv_detail', pk=ad.cv.pk)

# class Edit_ad(LoginRequiredMixin, UpdateView):
#     # fields = '__all__'
#     model = Academics
#     form_class = Academicsform
#     template_name = 'cvg/add_ad.html'
#     # def form_valid(self, form):
#     #     form.instance.created_by=self.request.user
#     #     return super().form_valid(form)

#comment section
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
        return render(request, 'cvg/addcomment.html', {'form': form})


@login_required
def remove_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('cvg:cv_detail', pk=comment.cv.pk)


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('cvg:cv_detail', pk=comment.cv.pk)





