## unused functions from last app
# @login_required
# def cv_draft_list(request):
#     cvs=Cv.objects.filter(published_date__isnull=True).order_by('-created_date')
#     context = {'cvs':cvs}
#     return render(request, 'cvg/cv_draft_list.html', context)

# @login_required
# def cv_publish(request, pk):
#     cv=get_object_or_404(Cv, pk=pk)
#     cv.published()
#     return redirect('cvg:cv_detail', pk=pk)