from django.urls import path
from . import views

app_name = 'cvg'

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('student/<int:pk>/', views.student_detail, name='student_detail'),
    path('student/new/', views.student_new, name='student_new'),
    path('student/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('student/<int:pk>/delete/', views.delete_student, name='delete_student'),
    path('draft/', views.student_draft_list, name='student_draft_list'),
    path('student/<int:pk>/publish/', views.student_publish, name='student_publish'),
    path('student/<int:pk>/comment/', views.add_comment_to_student, name='add_comment'),
    path('comment/<int:pk>/remove/', views.remove_comment, name='remove_comment'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='approve_comment'),
    
]