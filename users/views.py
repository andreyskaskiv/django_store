from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)  # Audit
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)  # Authentication
            if user:
                auth.login(request, user)  # Authorisation
                messages.success(request, 'You have successfully logged in!')
                return HttpResponseRedirect(reverse('index'))

    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data updated!')
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    context = {'title': 'Store - Profile',
               'form': form,
               'baskets': Basket.objects.filter(user=request.user)}
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    messages.success(request, 'Bye...')
    return HttpResponseRedirect(reverse('index'))
