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
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='jobs/login.html'), name='login'),
    path('profile/complete/', views.profile_complete, name='profile_complete'),
    path('logout/', views.logout_view, name='logout'),
    path('application/edit/<int:application_id>/', views.edit_application, name='edit_application'),
    path('application/delete/<int:application_id>/', views.delete_application, name='delete_application'),
    path('job/edit/<int:job_id>/', views.edit_job, name='edit_job'),
]
