from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .forms import AccountAuthenticationForm, AccountSignupForm, ResetPasswordForm
from authorization.models import Membership
from team.models import JoinRequest
from team.forms import JoinRequestForm

def signup(request):
    if request.user.is_authenticated:
        return redirect('user:dashboard', u_pk=request.user.pk)
    if request.method == 'POST':
        form = AccountSignupForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('user:dashboard', u_pk=request.user.pk)
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = AccountSignupForm()
        return render(request, 'signup.html', {'form': form})

def signin(request):
    user = request.user
    if user.is_authenticated:
        return redirect('user:dashboard', u_pk=request.user.pk)
    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('user:dashboard', u_pk=request.user.pk)
        else:
            return render(request, 'signin.html', {'form': form})
    else:
        form = AccountAuthenticationForm()
    return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('landing')

# def dashboard_view(request, user_id, join_form=None):
#     user = get_user_model().objects.values('email', 'first_name', 'last_name').get(pk=user_id)
#     teams = Membership.objects.filter(user_id=user_id).values('created_at', 'alumni', 'team_id__pk', 'team_id__name', 'role_id__pk', 'role_id__role_name')
#     join_requests = JoinRequest.objects.filter(user_id=user_id)
#     if not join_form:
#         join_form = JoinRequestForm()
#     return render(request, 'dashboard.html', {
#         'user': user, 
#         'teams': teams,
#         'join_requests': join_requests,
#         'join_form': join_form
#     })

@login_required(login_url='user:signin')
def dashboard(request, u_pk):
    user = get_user_model().objects.values('email', 'first_name', 'last_name').get(pk=u_pk)
    teams = Membership.objects.filter(user_id=u_pk).values('created_at', 'alumni', 'team_id__id', 'team_id__name', 'role_id__pk', 'role_id__role_name')
    join_requests = JoinRequest.objects.filter(user_id=u_pk)
    join_form = JoinRequestForm()
    join_form_errors = request.session.get('join_form_errors')
    if join_form_errors:
        for field, err in join_form_errors.items():
            join_form.errors[field] = err
        del request.session['join_form_errors']
    return render(request, 'dashboard.html', {
        'user': user, 
        'teams': teams,
        'join_requests': join_requests,
        'join_form': join_form
    })

@login_required(login_url='user:signin')
def accountsettings(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST, instance=request.user)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data.get('new_password1'))
            user.save()
            return redirect('user:dashboard', u_pk=request.user.pk)
        else:
            return render(request, 'settings.html', {'form': form})
    else:
        form = ResetPasswordForm(instance=request.user)
        return render(request, 'settings.html', {'form': form})

# @login_required(login_url='user:signin')
# def accountchange(request):
#     user = get_user_model().objects.values('email', 'first_name', 'last_name').get(pk=request.user.pk)
#     if user.check_password(request.POST['password']):
#         user.first_name = request.POST.get('first_name')
#         user.last_name = request.POST.get('last_name')
#         user.set_password(request.POST['new_password'])
#         user.save()
#         return redirect('user:dashboard', u_pk=request.user.pk)
#     else:
#         return render(request, 'settings.html', {'user': user, 'error': 'Incorrect password'})
