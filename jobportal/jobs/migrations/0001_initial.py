# Generated by Django 5.2 on 2025-04-11 05:33

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("website", models.URLField(blank=True)),
                ("logo", models.ImageField(blank=True, upload_to="company_logos/")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Job",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("location", models.CharField(max_length=100)),
                (
                    "job_type",
                    models.CharField(
                        choices=[
                            ("FT", "Full-time"),
                            ("PT", "Part-time"),
                            ("CN", "Contract"),
                            ("IN", "Internship"),
                        ],
                        max_length=2,
                    ),
                ),
                (
                    "posted_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("closing_date", models.DateTimeField()),
                ("is_active", models.BooleanField(default=True)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="jobs.company"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="JobSeeker",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("resume", models.FileField(blank=True, upload_to="resumes/")),
                ("skills", models.TextField(blank=True)),
                ("experience", models.TextField(blank=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Application",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "applied_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("AP", "Applied"),
                            ("RV", "Under Review"),
                            ("IT", "Interview"),
                            ("RJ", "Rejected"),
                            ("AC", "Accepted"),
                        ],
                        default="AP",
                        max_length=2,
                    ),
                ),
                ("cover_letter", models.TextField()),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="jobs.job"
                    ),
                ),
                (
                    "applicant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="jobs.jobseeker"
                    ),
                ),
            ],
            options={
                "unique_together": {("job", "applicant")},
            },
        ),
    ]
