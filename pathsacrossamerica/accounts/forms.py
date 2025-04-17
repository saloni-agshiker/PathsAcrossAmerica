from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from .models import SecurityQuestions

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert"> {e}</div>' for e in self]))

class CustomUserCreationForm(UserCreationForm):
    security_answer1 = forms.CharField(
        label="What city were you born in?",
        max_length=255,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    security_answer2 = forms.CharField(
        label="What is your mother's maiden name?",
        max_length=255,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                {'class': 'form-control'}
            )
        self.order_fields(['username', 'password1', 'password2', 'security_answer'])

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            SecurityQuestions.objects.create(
                user=user,
                security_answer1=self.cleaned_data['security_answer1'],
                security_answer2=self.cleaned_data['security_answer2'],
            )
        return user