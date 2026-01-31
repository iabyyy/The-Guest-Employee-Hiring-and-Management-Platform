from django.db import models
from django.contrib.auth.models import User


class ContractorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    requirements = models.TextField()
    registration_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class GuestEmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.CharField(max_length=200)
    experience = models.IntegerField()
    availability = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Job(models.Model):
    contractor = models.ForeignKey(ContractorProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='feedback_given'
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='feedback_received'
    )
    rating = models.IntegerField()
    comment = models.TextField()
