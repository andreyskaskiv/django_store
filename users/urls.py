from django.contrib.auth.decorators import login_required
from django.urls import path

from users.views import login, UserRegistrationView, UserProfileView, logout

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),  # ../users/login
    path('register/', UserRegistrationView.as_view(), name='register'),  # ../users/register
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),  # ../users/profile
    path('logout/', logout, name='logout'),

]
