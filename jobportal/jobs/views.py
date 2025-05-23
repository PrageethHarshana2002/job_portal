from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Company, JobSeeker, Job, Application
from .forms import (UserRegisterForm, JobForm, ApplicationForm, CompanyRegisterForm, JobSeekerRegisterForm)
from django.contrib.auth import logout
from django.db.models import Q
from django.core.paginator import Paginator

def home(request):
    jobs_list = Job.objects.filter(is_active=True).order_by('-posted_date')
    companies = Company.objects.all()[:12]

    # Handle search query
    search_query = request.GET.get('q')
    if search_query:
        jobs_list = jobs_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(company__name__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(jobs_list, 6)
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    return render(request, 'jobs/home.html', {
        'jobs': jobs,
        'companies': companies,
        'total_companies': Company.objects.count(),
        'total_jobseekers': JobSeeker.objects.count(),
        'total_jobs': Job.objects.filter(is_active=True).count(),
    })



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
    if hasattr(request.user, 'company'):
        jobs = Job.objects.filter(company=request.user.company).order_by('-posted_date')
        return render(request, 'jobs/company_dashboard.html', {'jobs': jobs})
    elif hasattr(request.user, 'jobseeker'):
        applications = Application.objects.filter(applicant=request.user.jobseeker).order_by('-applied_date')
        return render(request, 'jobs/jobseeker_dashboard.html', {'applications': applications})
    else:
        return redirect('home')

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    has_applied = False

    if hasattr(request.user, 'jobseeker'):
        has_applied = Application.objects.filter(job=job, applicant=request.user.jobseeker).exists()

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'has_applied': has_applied
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

@login_required
def edit_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, applicant=request.user.jobseeker)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ApplicationForm(instance=application)

    return render(request, 'jobs/edit_application.html', {
        'form': form,
        'application': application
    })


@login_required
def delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, applicant=request.user.jobseeker)

    if request.method == 'POST':
        application.delete()
        return redirect('dashboard')

    return render(request, 'jobs/confirm_application_delete.html', {'application': application})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, company=request.user.company)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/edit_job.html', {
        'form': form,
        'job': job
    })

def about(request):
    return render(request, 'jobs/about.html', )

@login_required
def profile(request):
    context = {}

    if hasattr(request.user, 'company'):
        context['profile_type'] = 'company'
        context['profile'] = request.user.company
    elif hasattr(request.user, 'jobseeker'):
        context['profile_type'] = 'jobseeker'
        context['profile'] = request.user.jobseeker

    return render(request, 'jobs/profile.html', context)

@login_required
def edit_company_profile(request):
    if not hasattr(request.user, 'company'):
        return redirect('home')

    company = request.user.company
    if request.method == 'POST':
        form = CompanyRegisterForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company profile updated successfully!')
            return redirect('profile')
    else:
        form = CompanyRegisterForm(instance=company)

    return render(request, 'jobs/edit_profile.html', {
        'form': form,
        'profile_type': 'company'
    })


@login_required
def edit_jobseeker_profile(request):
    if not hasattr(request.user, 'jobseeker'):
        return redirect('home')

    jobseeker = request.user.jobseeker
    if request.method == 'POST':
        form = JobSeekerRegisterForm(request.POST, request.FILES, instance=jobseeker)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job seeker profile updated successfully!')
            return redirect('profile')
    else:
        form = JobSeekerRegisterForm(instance=jobseeker)

    return render(request, 'jobs/edit_profile.html', {
        'form': form,
        'profile_type': 'jobseeker'
    })