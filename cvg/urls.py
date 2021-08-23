from django.urls import path
from . import views
# from cvg.views import Edit_ad

app_name = 'cvg'

urlpatterns = [
    path('', views.cv_list, name='cv_list'),
    path('cv/<int:pk>/', views.cv_detail, name='cv_detail'),
    path('cv/<int:pk>/preview', views.cv_preview, name='cv_preview'),
    
    # path('cv/<int:pk>/edit/', Cv_new.as_view(), name='cv_new'),
    path('cv/new/', views.cv_new, name='cv_new'),
    
    # path('cv/<int:pk>/edit/', Cv_edit.as_view(), name='cv_edit'),
    path('cv/<int:pk>/edit/', views.cv_edit, name='cv_edit'),
    
    path('cv/ad/<int:pk>/add', views.add_ad_to_cv, name='add_ad'),
    path('cv/ad/<int:pk>/remove/', views.remove_ad, name='remove_ad'),
    path('cv/ad/<int:pk>/unapprove/', views.unapprove_ad, name='unapprove_ad'),
    path('cv/ad/<int:pk>/edit/', views.edit_ad, name='edit_ad'),
    # path('cv/comment/<int:pk>/edit/', Edit_ad.as_view(), name='edit_ad'),

    path('cv/sd/<int:pk>/add', views.add_sd_to_cv, name='add_sd'),
    path('cv/sd/<int:pk>/remove/', views.remove_sd, name='remove_sd'),
    path('cv/sd/<int:pk>/unapprove/', views.unapprove_sd, name='unapprove_sd'),
    path('cv/sd/<int:pk>/edit/', views.edit_sd, name='edit_sd'),

    path('cv/ed/<int:pk>/add', views.add_ed_to_cv, name='add_ed'),
    path('cv/ed/<int:pk>/remove/', views.remove_ed, name='remove_ed'),
    path('cv/ed/<int:pk>/unapprove/', views.unapprove_ed, name='unapprove_ed'),
    path('cv/ed/<int:pk>/edit/', views.edit_ed, name='edit_ed'),

    path('cv/ind/<int:pk>/add', views.add_ind_to_cv, name='add_ind'),
    path('cv/ind/<int:pk>/remove/', views.remove_ind, name='remove_ind'),
    path('cv/ind/<int:pk>/unapprove/', views.unapprove_ind, name='unapprove_ind'),
    path('cv/ind/<int:pk>/edit/', views.edit_ind, name='edit_ind'),

    path('cv/pd/<int:pk>/add', views.add_pd_to_cv, name='add_pd'),
    path('cv/pd/<int:pk>/remove/', views.remove_pd, name='remove_pd'),
    path('cv/pd/<int:pk>/unapprove/', views.unapprove_pd, name='unapprove_pd'),
    path('cv/pd/<int:pk>/edit/', views.edit_pd, name='edit_pd'),

    path('cv/rd/<int:pk>/add', views.add_rd_to_cv, name='add_rd'),
    path('cv/rd/<int:pk>/remove/', views.remove_rd, name='remove_rd'),
    path('cv/rd/<int:pk>/unapprove/', views.unapprove_rd, name='unapprove_rd'),
    path('cv/rd/<int:pk>/edit/', views.edit_rd, name='edit_rd'),

    path('cv/<int:pk>/delete/', views.delete_cv, name='delete_cv'),
    path('draft/', views.cv_draft_list, name='cv_draft_list'),
    path('cv/<int:pk>/publish/', views.cv_publish, name='cv_publish'),
    path('cv/<int:pk>/comment/', views.add_comment_to_cv, name='add_comment'),
    path('comment/<int:pk>/remove/', views.remove_comment, name='remove_comment'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='approve_comment'),

]