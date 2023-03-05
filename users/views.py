from django.contrib import auth, messages
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User


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


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data()
        context['title'] = 'Store - Registration'
        return context


# messages.success(request, 'You have successfully registered!')

class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Profile'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['title'] = 'Store - Profile'
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context


# messages.success(request, 'Data updated!')


def logout(request):
    auth.logout(request)
    messages.success(request, 'Bye...')
    return HttpResponseRedirect(reverse('index'))
