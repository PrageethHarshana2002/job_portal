from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Company, JobSeeker, Job, Application
from .forms import (UserRegisterForm,JobForm)

def home(request):
    jobs = Job.objects.filter(is_active=True).order_by('-posted_date')[:10]
    return render(request, 'jobs/home.html', {'jobs': jobs})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please complete your profile.')
            return redirect('profile_complete')
    else:
        form = UserRegisterForm()
    return render(request, '#', {'form': form})

@login_required

def dashboard(request):
    if hasattr(request.user, ''):
        jobs = Job.objects.filter(company=request.user.company).order_by('-posted_date')
        return render(request, 'jobs/company_dashboard.html', {'jobs': jobs})
    elif hasattr(request.user, ''):
        applications = Application.objects.filter(applicant=request.user.jobseeker).order_by('-applied_date')
        return render(request, 'jobs/jobseeker_dashboard.html', {'applications': applications})
    else:
        pass

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    return render(request, 'jobs/job_detail.html', {
        'job': job,
    })


@login_required
def post_job(request):
    if not hasattr(request.user, 'company'):
        return redirect('home')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.company
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('dashboard')
    else:
        form = JobForm()

    return render(request, 'jobs/post_job.html', {'form': form})

