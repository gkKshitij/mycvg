from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Academics, Cv, Comment, Skills, Extracurricular, Internships, Projects, Roles
from .forms import Cvform, Commentform, UserForm, Academicsform, Skillsform, Extracurricularform, Internshipsform, \
    Projectsform, Rolesform
from .custom import *
from mycvg.settings import *

import os
# import subprocess
from django.http import FileResponse

from subprocess import call
from tempfile import mkdtemp, mkstemp
from django.template.loader import render_to_string
import shutil 
  

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


# comment section
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


# actual start of useful stuff
# csddct = dctc(dct)
def dctc(dct):
    """dictionary cleaner removes null/blank values"""
    null = ""
    cdct = {k: v for k, v in dct.items() if v != null}
    # print(cdct)
    return cdct


# sefunc('mst', csddct)
def sefunc(textemplate, rdct):  # use only for skills and extracurricular
    """
    takes string template and raw dictionary and renders after substitution only
    """
    dct = dctc(rdct)
    with open(f'cvg/static/cvg/{textemplate}.tex', 'r') as template:

        # print(len(dct.keys()))
        d = template.read()  # .replace('first_name','Kshitij') #.split()
        print('Template loaded:')  # Print template for visual cue.

    key_list = list(dct.keys())
    val_list = list(dct.values())

    com = [sub.replace(sub, '%' + sub) for sub in key_list]
    com_dct = {com[i]: " " for i in range(len(com))}

    for key, value in com_dct.items():
        d = d.replace(key, str(value))  # Replace comments key character with null/space

    # print(com_dct)

    res = [sub.replace(sub, 'kk' + sub) for sub in key_list]
    res_dct = {res[i]: val_list[i] for i in range(len(res))}

    # bkp manual method
    for key, value in res_dct.items():
        d = d.replace(key, str(value))  # Replace key character with value character in string

    # print(d)
    return d


# iprf('r_prot', dct)
def iprfunc(textemplate, dct, hstr):  # use only for internships,projects,roles
    """
    takes string template and dictionary object for rendering after substitution only
    """

    with open(f'cvg/static/cvg/{textemplate}.tex', 'r') as template:

        # print(len(dct.keys()))
        d = template.read()  # .replace('first_name','Kshitij') #.split()
        print('Template loaded:')  # Print template for visual cue.

    # for i in pd:
    #     dct=i

    key_list = list(dct.keys())
    val_list = list(dct.values())
    prefix = "\kkkresumeItem{"

    temp_desc = (dct['description']).split('\n')
    # print(len(temp_desc))
    mod_desc = ''
    for aline in temp_desc:
        # print(aline)
        mod_desc = mod_desc + prefix + aline + '}\t'

    d = d.replace('description', mod_desc)
    d = d.replace('kkk', "")
    res = [sub.replace(sub, 'kk' + sub) for sub in key_list]
    res_dct = {res[i]: val_list[i] for i in range(len(res))}
    # res_dct['kdescription'] = mod_desc
    # print(mod_desc)

    # bkp manual method
    for key, value in res_dct.items():
        d = d.replace(key, str(value))  # Replace key character with value character in string
    hstr = hstr + d
    # print(d)
    return hstr


# preview cv
def cv_preview(request, pk):
    cv = get_object_or_404(Cv, pk=pk)
    dcv_id = cv.id
    # null=""

    internships_c = 0
    projects_c = 0
    roles_c = 0

    ad = get_object_or_404(Academics, cv_id=dcv_id)

    cvd = cv.__dict__
    ad_d = ad.__dict__

    cdict = {**cvd, **ad_d}
    # cvs = Cv.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    final = sefunc('base', cdict)

    sd = get_object_or_404(Skills, cv_id=dcv_id)
    ed = get_object_or_404(Extracurricular, cv_id=dcv_id)

    # skill string maker
    if bool(sd):
        sd_d = sd.__dict__
        sd_str = sefunc('pst', sd_d)
        final = final + "\n" + sd_str

    # extracurricular string maker
    if bool(ed):
        ed_d = ed.__dict__
        ed_str = sefunc('mst', ed_d)
        final = final + "\n" + ed_str

    # internship string maker
    ind = Internships.objects.filter(cv_id=dcv_id).order_by('end_year' and 'end_month')
    if bool(ind):
        ind_str = "\section{Internships}"
        for i in ind:
            internships_c += 1
            tidct = i.__dict__
            ind_str = iprfunc('r_irt', tidct, ind_str)
        final = final + "\n" + ind_str

    # projects string maker
    pd = Projects.objects.filter(cv_id=dcv_id).order_by('end_year' and 'end_month')
    if bool(pd):
        pd_str = "\section{Projects}"
        for j in pd:
            projects_c += 1
            tjdct = j.__dict__
            pd_str = iprfunc('r_prot', tjdct, pd_str)
        final = final + "\n" + pd_str

    rd = Roles.objects.filter(cv_id=dcv_id).order_by('end_year' and 'end_month')
    if bool(rd):
        rd_str = "\section{Roles}"
        for k in rd:
            roles_c += 1
            tkdct = k.__dict__
            rd_str = iprfunc('r_irt', tkdct, rd_str)
        final = final + "\n" + rd_str

    suffix="\end{document}"
    final = final + suffix
    filename = str(cv.sap_id)
    #
    #
    #
    # make_pdf()
    destination = STATIC_ROOT
    tmp_folder = mkdtemp()
    os.chdir(tmp_folder) 
    
    f = open(f"{filename}.tex", "w")
    f.write(final)
    f.close()
    
    texfilename = filename+".tex"
    
    texfile, texfilename = mkstemp(dir=tmp_folder)
    
    call(['pdflatex', texfilename])
    
    # os.rename(f'{texfilename}.pdf',tmp_folder) #f'{filename}.pdf') #, destination)
    
    source = os.path.join( tmp_folder, texfilename+'.pdf')
    k = shutil.move(source, destination, copy_function = shutil.copytree) 
    
    os.remove(texfilename)
    os.remove(texfilename + '.aux')
    os.remove(texfilename + '.log')
    os.rmdir(tmp_folder)
    
    fp = os.path.join( STATIC_ROOT, texfilename+'.pdf')
    return FileResponse(open(fp, 'rb'), content_type='application/pdf')
    
    # cwd = os.getcwd()  # current working directory
    # stdir = STATIC_ROOT #os.path.join(cwd, "cvg\static\cvg")  # "test.tex") # static directory
    # fp = os.path.join(cwd, "cvg\static\cvg", f"{filename}.pdf")
    
    # os.chdir(STATIC_ROOT)

    # # try:
    # #     os.remove(f"{filename}.pdf")
    # # except:
    # #     pass
    # # finally:
    # #     print("reached here")

    # f = open(f"{filename}.tex", "w")
    # f.write(final)
    # f.close()

    # subprocess.check_call(['pdflatex', '-interaction=nonstopmode', f'{filename}.tex'])
    # os.remove(f"{filename}.aux")
    # os.remove(f"{filename}.log")
    # os.remove(f"{filename}.out")
    # os.chdir(BASE_DIR)
    
    # fp = os.path.join( STATIC_ROOT, f"{filename}.pdf")
    # return FileResponse(open(fp, 'rb'), content_type='application/pdf')


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
                cvd.modified_date = timezone.now()
                cvd.edited_by = request.user
                cvd.save()
                return redirect('cvg:cv_detail', pk=cvd.pk)
            except:
                return HttpResponse("Please maintain only one Cv")
                # TODO: make this later          
    else:
        form = Cvform()
    return render(request, 'cvg/form.html', {'form': form})


## generic form of above view
# class Cv_new(LoginRequiredMixin, CreateView):
#     # fields = '__all__'
#     model = Cv
#     form_class = Cvform
#     template_name = 'cvg/cv_edit.html'
#     def form_valid(self, form):
#         form.instance.created_by=self.request.user
#         return super().form_valid(form)

@login_required
def delete_cv(request, pk):
    cv = get_object_or_404(Cv, pk=pk)
    cv.delete()
    # context = {'cvs': cvs}
    return redirect('cvg:cv_list')


# edit cv basic details
@login_required
def cv_edit(request, pk):
    cv = get_object_or_404(Cv, pk=pk)
    if request.method == 'POST':
        form = Cvform(request.POST, instance=cv)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.edited_by = str(request.user)
            cv.modified_date = timezone.now()
            cv.edited_by = str(request.user)
            cv.save()
            return redirect('cvg:cv_detail', pk=cv.pk)
    else:
        form = Cvform(instance=cv)
    return render(request, 'cvg/form.html', {'form': form})


# # generic form of above view
# class Cv_edit(LoginRequiredMixin, UpdateView):
#     # fields = '__all__'
#     model = Cv
#     form_class = Cvform
#     template_name = 'cvg/cv_edit.html'
#     def form_valid(self, form):
#         form.instance.created_by=self.request.user
#         return super().form_valid(form)


# ad=academic details and views related to that

# class Edit_ad(LoginRequiredMixin, UpdateView):
#     # fields = '__all__'
#     model = Academics
#     form_class = Academicsform
#     template_name = 'cvg/add_ad.html'
#     # def form_valid(self, form):
#     #     form.instance.created_by=self.request.user
#     #     return super().form_valid(form)
@login_required
def add_ad_to_cv(request, pk):
    cv = get_object_or_404(Cv, pk=pk)
    if request.method == 'POST':
        form = Academicsform(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.edited_by = str(request.user)
            ad.modified_date = timezone.now()
            ad.cv = cv
            ad.save()
            return redirect('cvg:cv_detail', pk=cv.pk)
    else:
        form = Academicsform()
    return render(request, 'cvg/form.html', {'form': form})


@login_required
def edit_ad(request, pk):
    ad = get_object_or_404(Academics, pk=pk)
    if request.method == 'POST':
        form = Academicsform(request.POST, instance=ad)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.edited_by = str(request.user)
            ad.modified_date = timezone.now()
            ad.save()
            return redirect('cvg:cv_detail', pk=ad.cv.pk)
    else:
        form = Academicsform(instance=ad)
    return render(request, 'cvg/form.html', {'form': form})


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


# skills section
@login_required
def add_sd_to_cv(request, pk):
    cv = get_object_or_404(Cv, pk=pk)
    if request.method == 'POST':
        form = Skillsform(request.POST)
        if form.is_valid():
            sd = form.save(commit=False)
            sd.edited_by = str(request.user)
            sd.modified_date = timezone.now()
            sd.cv = cv
            sd.save()
            return redirect('cvg:cv_detail', pk=cv.pk)
    else:
        form = Skillsform()
    return render(request, 'cvg/form.html', {'form': form})


@login_required
def edit_sd(request, pk):
    sd = get_object_or_404(Skills, pk=pk)
    if request.method == 'POST':
        form = Skillsform(request.POST, instance=sd)
        if form.is_valid():
            sd = form.save(commit=False)
            sd.edited_by = str(request.user)
            sd.modified_date = timezone.now()
            sd.save()
            return redirect('cvg:cv_detail', pk=sd.cv.pk)
    else:
        form = Skillsform(instance=sd)
    return render(request, 'cvg/form.html', {'form': form})


@login_required
def remove_sd(request, pk):
    sd = get_object_or_404(Skills, pk=pk)
    sd.delete()
    return redirect('cvg:cv_detail', pk=sd.cv.pk)


@login_required
def unapprove_sd(request, pk):
    sd = get_object_or_404(Skills, pk=pk)
    sd.unapprove()
    return redirect('cvg:cv_detail', pk=sd.cv.pk)


# Extracurricular section
@login_required
def add_ed_to_cv(request, pk):
    cv = get_object_or_404(Cv, pk=pk)
    if request.method == 'POST':
        form = Extracurricularform(request.POST)
        if form.is_valid():
            ed = form.save(commit=False)
            ed.edited_by = str(request.user)
            ed.modified_date = timezone.now()
            ed.cv = cv
            ed.save()
            return redirect('cvg:cv_detail', pk=cv.pk)
    else:
        form = Extracurricularform()
    return render(request, 'cvg/form.html', {'form': form})


@login_required
def edit_ed(request, pk):
    ed = get_object_or_404(Extracurricular, pk=pk)
    if request.method == 'POST':
        form = Extracurricularform(request.POST, instance=ed)
        if form.is_valid():
            ed = form.save(commit=False)
            ed.edited_by = str(request.user)
            ed.modified_date = timezone.now()
            ed.save()
            return redirect('cvg:cv_detail', pk=ed.cv.pk)
    else:
        form = Extracurricularform(instance=ed)
    return render(request, 'cvg/form.html', {'form': form})


@login_required
def remove_ed(request, pk):
    ed = get_object_or_404(Extracurricular, pk=pk)
    ed.delete()
    return redirect('cvg:cv_detail', pk=ed.cv.pk)


@login_required
def unapprove_ed(request, pk):
    ed = get_object_or_404(Extracurricular, pk=pk)
    ed.unapprove()
    return redirect('cvg:cv_detail', pk=ed.cv.pk)


# Internship section
@login_required
def add_ind_to_cv(request, pk):
    cv = get_object_or_404(Cv, pk=pk)
    if request.method == 'POST':
        form = Internshipsform(request.POST)
        if form.is_valid():
            ind = form.save(commit=False)
            ind.edited_by = str(request.user)
            ind.modified_date = timezone.now()
            ind.cv = cv
            ind.save()
            return redirect('cvg:cv_detail', pk=cv.pk)
    else:
        form = Internshipsform()
    return render(request, 'cvg/form.html', {'form': form})


@login_required
def edit_ind(request, pk):
    ind = get_object_or_404(Internships, pk=pk)
    if request.method == 'POST':
        form = Internshipsform(request.POST, instance=ind)
        if form.is_valid():
            ind = form.save(commit=False)
            ind.edited_by = str(request.user)
            ind.modified_date = timezone.now()
            ind.save()
            return redirect('cvg:cv_detail', pk=ind.cv.pk)
    else:
        form = Internshipsform(instance=ind)
    return render(request, 'cvg/form.html', {'form': form})


@login_required
def remove_ind(request, pk):
    ind = get_object_or_404(Internships, pk=pk)
    ind.delete()
    return redirect('cvg:cv_detail', pk=ind.cv.pk)


@login_required
def unapprove_ind(request, pk):
    ind = get_object_or_404(Internships, pk=pk)
    ind.unapprove()
    return redirect('cvg:cv_detail', pk=ind.cv.pk)


# Projects section
@login_required
def add_pd_to_cv(request, pk):
    cv = get_object_or_404(Cv, pk=pk)
    if request.method == 'POST':
        form = Projectsform(request.POST)
        if form.is_valid():
            pd = form.save(commit=False)
            pd.edited_by = str(request.user)
            pd.modified_date = timezone.now()
            pd.cv = cv
            pd.save()
            return redirect('cvg:cv_detail', pk=cv.pk)
    else:
        form = Projectsform()
    return render(request, 'cvg/form.html', {'form': form})


@login_required
def edit_pd(request, pk):
    pd = get_object_or_404(Projects, pk=pk)
    if request.method == 'POST':
        form = Projectsform(request.POST, instance=pd)
        if form.is_valid():
            pd = form.save(commit=False)
            pd.edited_by = str(request.user)
            pd.modified_date = timezone.now()
            pd.save()
            return redirect('cvg:cv_detail', pk=pd.cv.pk)
    else:
        form = Projectsform(instance=pd)
    return render(request, 'cvg/form.html', {'form': form})


@login_required
def remove_pd(request, pk):
    pd = get_object_or_404(Projects, pk=pk)
    pd.delete()
    return redirect('cvg:cv_detail', pk=pd.cv.pk)


@login_required
def unapprove_pd(request, pk):
    pd = get_object_or_404(Projects, pk=pk)
    pd.unapprove()
    return redirect('cvg:cv_detail', pk=pd.cv.pk)


# Roles section
@login_required
def add_rd_to_cv(request, pk):
    cv = get_object_or_404(Cv, pk=pk)
    if request.method == 'POST':
        form = Rolesform(request.POST)
        if form.is_valid():
            rd = form.save(commit=False)
            rd.edited_by = str(request.user)
            rd.modified_date = timezone.now()
            rd.cv = cv
            rd.save()
            return redirect('cvg:cv_detail', pk=cv.pk)
    else:
        form = Rolesform()
    return render(request, 'cvg/form.html', {'form': form})


@login_required
def edit_rd(request, pk):
    rd = get_object_or_404(Roles, pk=pk)
    if request.method == 'POST':
        form = Rolesform(request.POST, instance=rd)
        if form.is_valid():
            rd = form.save(commit=False)
            rd.edited_by = str(request.user)
            rd.modified_date = timezone.now()
            rd.save()
            return redirect('cvg:cv_detail', pk=rd.cv.pk)
    else:
        form = Rolesform(instance=rd)
    return render(request, 'cvg/form.html', {'form': form})


@login_required
def remove_rd(request, pk):
    rd = get_object_or_404(Roles, pk=pk)
    rd.delete()
    return redirect('cvg:cv_detail', pk=rd.cv.pk)


@login_required
def unapprove_rd(request, pk):
    rd = get_object_or_404(Roles, pk=pk)
    rd.unapprove()
    return redirect('cvg:cv_detail', pk=rd.cv.pk)
