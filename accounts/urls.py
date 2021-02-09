from django.urls import path
from .views import Login, Logout, Register, Profile, UpdateProfile

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('<int:pk>/profile/', Profile.as_view(), name='profile'),
    path('<int:pk>/profile/update', UpdateProfile.as_view(), name='update-profile'),
]
