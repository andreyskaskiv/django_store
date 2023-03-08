from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth.views import LogoutView

from users.views import UserLoginView, UserRegistrationView, UserProfileView, EmailVerificationView, IndexView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),  # ../users/login
    path('register/', UserRegistrationView.as_view(), name='register'),  # ../users/register
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),  # ../users/profile/1
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),

    path('service/', IndexView.as_view(), name='service'),  # ../users/service

]
