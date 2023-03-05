from django.urls import path

from users.views import login, UserRegistrationView, profile, logout

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),  # ../users/login
    path('register/', UserRegistrationView.as_view(), name='register'),  # ../users/register
    path('profile/', profile, name='profile'),  # ../users/profile
    path('logout/', logout, name='logout'),

]
