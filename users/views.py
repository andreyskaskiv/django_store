from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, GenerateDataForm
from users.models import User, EmailVerification

from tools.db_manager import main as write_to_db_test_data


class UserLoginView(TitleMixin, SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_message = 'You have successfully logged in!'
    title = 'Store - Login'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    title = 'Store - Registration'
    success_url = reverse_lazy('users:login')
    success_message = 'You have successfully registered!'


class UserProfileView(TitleMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Profile'
    success_message = 'Data updated!'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Email confirmation'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


class DataGenerationView(TitleMixin, SuccessMessageMixin, FormView):
    title = 'Store - Data generation'
    template_name = 'users/service.html'
    form_class = GenerateDataForm
    success_url = reverse_lazy('users:service')
    success_message = 'Data updated!'

    def form_valid(self, form):
        quantity = form.cleaned_data['quantity']
        # add user profile generation

        write_to_db_test_data()

        return super().form_valid(form)
