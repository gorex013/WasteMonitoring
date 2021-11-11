from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

username_validator = UnicodeUsernameValidator()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label=_('First Name'), max_length=12, min_length=1,
                                 required=True,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'placeholder': 'Your first name',
                                         'data-toggle': 'tooltip',
                                         'data-placement': 'right',
                                         'title': 'We would like to call you by full name.'
                                     }))
    last_name = forms.CharField(label=_('Last name'), max_length=12, min_length=1, required=True,
                                widget=(
                                    forms.TextInput(attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Your last name',
                                        'data-toggle': 'tooltip',
                                        'data-placement': 'right',
                                        'title': 'We would like to call you by full name.'
                                    })))
    password1 = forms.CharField(label=_('Password'),
                                widget=(forms.PasswordInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'Password',
                                                                   'data-toggle': 'tooltip',
                                                                   'data-placement': 'right',
                                                                   'title': 'Your password must be secure.'
                                                                   })
                                        ),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label=_('Password Confirmation'),
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Password confirmation',
                                           'data-toggle': 'tooltip',
                                           'data-placement': 'right',
                                           'title': 'Password need to be the same'
                                           }),
                                help_text=_('Just Enter the same password, for confirmation'))
    username = forms.EmailField(
        label=_('E-mail'),
        max_length=150,
        validators=[username_validator],
        error_messages={'unique': _("A user with that username already exists.")},
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Your e-mail',
                                      'data-toggle': 'tooltip',
                                      'data-placement': 'right',
                                      'title': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
                                      })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2',)
