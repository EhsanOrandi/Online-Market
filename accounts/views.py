from django.shortcuts import render, reverse, redirect
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegisterationForm
from .models import User, Shop, Address
from products.models import Category
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect

# Create your views here.

class Login(LoginView):
    template_name = "components/login.html"
    redirect_field_name = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent__isnull=True)
        return context

class Logout(LogoutView):
    pass

# def register_view(request):
#     if request.method == 'GET':
#         form = UserRegisterationForm()
#     else:
#         form = UserRegisterationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data.get('password'))
#             form.save()
#             return redirect('login')

#     context = {
#         'form': form,
#     }
#     return render(request, 'components/register.html', context=context)

class Register(CreateView, SuccessMessageMixin):
    template_name = 'components/register.html'
    form_class = UserRegisterationForm
    success_url = '/user/login/'
    success_message = 'Your account was created successfully.'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password'))
        form.save()
        return HttpResponseRedirect(self.success_url)

class Profile(DetailView):
    model = User
    template_name = 'components/profile.html'

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        user = context.get('user', None)
        context['address'] = Address.objects.filter(user=user)
        context['shops'] = Shop.objects.filter(user=user) 
        context['categories'] = Category.objects.filter(parent__isnull=True)
        return context

class UpdateProfile(UpdateView):
    model = User
    fields = ['email', 'first_name', 'last_name', 'mobile', 'avatar']
    template_name = 'components/update-profile.html'

    def get_success_url(self):
        return reverse('profile', args = (self.object.id,))
