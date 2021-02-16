from django.shortcuts import render, reverse
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegisterationForm
from .models import User, Shop, Address
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.

class Login(LoginView):
    template_name = "components/login.html"
    redirect_field_name = '/'

class Logout(LogoutView):
    pass

class Register(CreateView, SuccessMessageMixin):
    template_name = 'components/register.html'
    form_class = UserRegisterationForm
    success_url = '/user/login/'
    success_message = 'Your account was created successfully.'

class Profile(DetailView):
    model = User
    template_name = 'components/profile.html'

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        user = context.get('user', None)
        context['address'] = Address.objects.filter(user=user)
        context['shops'] = Shop.objects.filter(user=user) 
        return context

class UpdateProfile(UpdateView):
    model = User
    fields = ['email', 'first_name', 'last_name', 'mobile', 'avatar']
    template_name = 'components/update-profile.html'

    def get_success_url(self):
        return reverse('profile', args = (self.object.id,))
