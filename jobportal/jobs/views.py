from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Company, JobSeeker, Job, Application
from .forms import (UserRegisterForm, JobForm, ApplicationForm, CompanyRegisterForm, JobSeekerRegisterForm)
from django.contrib.auth import logout

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
    return render(request, 'jobs/register.html', {'form': form})

@login_required

def dashboard(request):
    if hasattr(request.user, ''):
        jobs = Job.objects.filter(company=request.user.company).order_by('-posted_date')
        return render(request, 'jobs/company_dashboard.html', {'jobs': jobs})
    elif hasattr(request.user, ''):
        applications = Application.objects.filter(applicant=request.user.jobseeker).order_by('-applied_date')
        return render(request, 'jobs/jobseeker_dashboard.html', {'applications': applications})
    else:
        return redirect('home')

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


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)

    if not hasattr(request.user, 'jobseeker'):
        messages.warning(request, 'Only job seekers can apply for jobs.')
        return redirect('job_detail', job_id=job_id)

    if Application.objects.filter(job=job, applicant=request.user.jobseeker).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', job_id=job_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user.jobseeker
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('job_detail', job_id=job_id)
    else:
        form = ApplicationForm()

    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})


@login_required
def view_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, company=request.user.company)
    applications = Application.objects.filter(job=job).select_related('applicant__user').order_by('-applied_date')

    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        if application_id and new_status:
            application = get_object_or_404(Application, id=application_id, job=job)
            application.status = new_status
            application.save()
            messages.success(request, 'Application status updated successfully!')
            return redirect('view_applications', job_id=job.id)

    return render(request, 'jobs/view_applications.html', {
        'job': job,
        'applications': applications
    })

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, company=request.user.company)

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job post deleted successfully!')
        return redirect('dashboard')

    return render(request, 'jobs/confirm_delete_job.html', {'job': job})

@login_required
def profile_complete(request):
    if hasattr(request.user, 'company') or hasattr(request.user, 'jobseeker'):
        return redirect('home')

    if request.method == 'POST':
        if 'company' in request.POST:
            company_form = CompanyRegisterForm(request.POST, request.FILES)
            if company_form.is_valid():
                company = company_form.save(commit=False)
                company.user = request.user
                company.save()
                messages.success(request, 'Company profile completed!')
                return redirect('home')
        else:
            jobseeker_form = JobSeekerRegisterForm(request.POST, request.FILES)
            if jobseeker_form.is_valid():
                jobseeker = jobseeker_form.save(commit=False)
                jobseeker.user = request.user
                jobseeker.save()
                messages.success(request, 'Job seeker profile completed!')
                return redirect('home')
    else:
        company_form = CompanyRegisterForm()
        jobseeker_form = JobSeekerRegisterForm()

    return render(request, 'jobs/profile_complete.html', {
        'company_form': company_form,
        'jobseeker_form': jobseeker_form
    })

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'jobs/logout.html')