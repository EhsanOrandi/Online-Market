from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField(label=_("Email"), required=True, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control my- 2'}))
    password = forms.CharField(label=_("Password"), required=True, widget=forms.PasswordInput(attrs={'class': 'form-control my- 2'})) 

class UserRegisterationForm(forms.ModelForm):
    password2 = forms.CharField(label=_('Repeat password'), required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        password = self.cleaned_data.get('password', None)
        password2 = self.cleaned_data.get('password2', None)
        print(password, password2)
        if password != password2:
            raise ValidationError(_("Password and its confirmation don't match"), code='invalid')