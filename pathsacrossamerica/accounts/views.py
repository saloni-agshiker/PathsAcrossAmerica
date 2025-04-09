from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import SecurityQuestions
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] ='The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST,
                                      error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                          {'template_data': template_data})

def request_reset(request):
    template_data = {}
    template_data['title'] = 'Request Reset'
    if request.method == 'GET':
        return render(request, 'accounts/request_reset.html',
               {'template_data': template_data})
    elif request.method == 'POST':
        try:
            username = request.POST['username']
            security_answer1 = request.POST.get('security_answer1')
            security_answer2 = request.POST.get('security_answer2')
            correct_answers = SecurityQuestions.objects.get(user=User.objects.get(username=username))
            if check_password(security_answer1, correct_answers.security_answer1) and check_password(security_answer2, correct_answers.security_answer2):
                token = default_token_generator.make_token(user=User.objects.get(username=username))
                url = reverse('accounts.password_reset', args=[username, token])
                return redirect(url)
            else:
                template_data['error'] = 'At least one of the answers is incorrect.'
                return render(request, 'accounts/request_reset.html', {'template_data': template_data})
        except User.DoesNotExist:
            template_data['error'] = 'This user does not exist.'
            return render(request, 'accounts/request_reset.html', {'template_data': template_data})

def password_reset(request, username, token):
    template_data = {}
    template_data['title'] = 'Password Reset'
    if request.method == 'GET':
        return render(request, 'accounts/password_reset.html',
                      {'template_data': template_data})
    try:
        user = User.objects.get(username=username)
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    new_password = form.cleaned_data['new_password1']
                    user.set_password(new_password)
                    user.save()
                    return render(request, 'accounts/login.html',
                                      {'template_data': template_data})
                else:
                    return render(request, 'accounts/password_reset.html',
                                  {'template_data': template_data, 'form': form})
                # return render(request, 'accounts/password_reset.html', {'template_data': template_data, 'form': form})
            else:
                template_data['error'] = 'Invalid reset token.'
                return render(request, 'accounts/password_reset.html', {'template_data': template_data})
    except User.DoesNotExist:
        template_data['error'] = 'Invalid user.'
        return render(request, 'accounts/password_reset.html', {'template_data': template_data})
    return render(request, 'accounts/password_reset.html', {'template_data': template_data})