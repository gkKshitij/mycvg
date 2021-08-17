from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('draft/', views.post_draft_list, name='post_draft_list'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment'),
    path('comment/<int:pk>/remove/', views.remove_comment, name='remove_comment'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='approve_comment'),
    
]