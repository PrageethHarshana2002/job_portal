from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Company, JobSeeker, Job, Application

from .forms import (UserRegisterForm)


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
        return render(request, 'jobs/jobseeker_dashboard.html', {'applications': applications})






