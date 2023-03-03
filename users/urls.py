from django.urls import path

from users.views import login, register, profile, logout

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),  # ../users/login
    path('register/', register, name='register'),  # ../users/register
    path('profile/', profile, name='profile'),  # ../users/profile
    path('logout/', logout, name='logout'),

]
