from django.urls import path
from . import views

app_name = 'cvg'

urlpatterns = [
    path('', views.cv_list, name='cv_list'),
    path('cv/<int:pk>/', views.cv_detail, name='cv_detail'),
    path('cv/new/', views.cv_new, name='cv_new'),
    path('cv/<int:pk>/edit/', views.cv_edit, name='cv_edit'),
    path('cv/<int:pk>/delete/', views.delete_cv, name='delete_cv'),
    path('draft/', views.cv_draft_list, name='cv_draft_list'),
    path('cv/<int:pk>/publish/', views.cv_publish, name='cv_publish'),
    path('cv/<int:pk>/comment/', views.add_comment_to_cv, name='add_comment'),
    path('comment/<int:pk>/remove/', views.remove_comment, name='remove_comment'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='approve_comment'),
    
]