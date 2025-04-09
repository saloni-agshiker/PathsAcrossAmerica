from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class SecurityQuestions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    security_answer1 = models.CharField(max_length=255)
    security_answer2 = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.security_answer1 = make_password(self.security_answer1)
        self.security_answer2 = make_password(self.security_answer2)
        super().save(*args, **kwargs)