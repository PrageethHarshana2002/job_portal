from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('post-job/', views.post_job, name='post_job'),
    path('job/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('job/<int:job_id>/applications/', views.view_applications, name='view_applications'),
    path('job/<int:job_id>/delete/', views.delete_job, name='delete_job'),

]
