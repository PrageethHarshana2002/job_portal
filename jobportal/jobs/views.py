from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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




