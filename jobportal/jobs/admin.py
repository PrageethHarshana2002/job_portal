from django.contrib import admin
from .models import Company, JobSeeker, Job, Application

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'website')
    search_fields = ('name', 'user__username')

@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('user', 'skills')
    search_fields = ('user__username', 'skills')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'posted_date', 'closing_date', 'is_active')
    list_filter = ('job_type', 'is_active', 'posted_date')
    search_fields = ('title', 'company__name', 'description')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'applied_date', 'status')
    list_filter = ('status', 'applied_date')
    search_fields = ('job__title', 'applicant__user__username')