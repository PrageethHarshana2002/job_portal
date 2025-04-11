from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Application(models.Model):
    STATUS_CHOICES = [
        ('AP', 'Applied'),
        ('RV', 'Under Review'),
        ('IT', 'Interview'),
        ('RJ', 'Rejected'),
        ('AC', 'Accepted'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='AP')
    cover_letter = models.TextField()

    class Meta:
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f"{self.applicant} application for {self.job}"

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', blank=True)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True)

    def _str_(self):
        return self.name