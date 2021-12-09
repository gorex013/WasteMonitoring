from datetime import date

from django import forms
from django.contrib.auth import validators
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.core.validators import MinValueValidator
from django.forms import models
from django.forms.formsets import DEFAULT_MIN_NUM, MIN_NUM_FORM_COUNT
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

from waste_monitoring.models import WasteData, WasteType

username_validator = UnicodeUsernameValidator()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label=_('Prenumele'), max_length=12, min_length=1,
                                 required=True,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'placeholder': 'Prenumele',
                                         'data-toggle': 'tooltip',
                                         'data-placement': 'right',
                                         'title': 'Am dori să știm cum să ne adresăm la dumneavoastră.'
                                     }))
    last_name = forms.CharField(label=_('Numele'), max_length=12, min_length=1, required=True,
                                widget=(
                                    forms.TextInput(attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Numele',
                                        'data-toggle': 'tooltip',
                                        'data-placement': 'right',
                                        'title': 'Am dori să știm cum să ne adresăm la dumneavoastră.'
                                    })))
    password1 = forms.CharField(label=_('Parola'),
                                widget=(forms.PasswordInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'Parola',
                                                                   'data-toggle': 'tooltip',
                                                                   'data-placement': 'right',
                                                                   'title': 'Parola trebuie să fie securizată.'
                                                                   })
                                        ),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label=_('Password Confirmation'),
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Confirmare parolă',
                                           'data-toggle': 'tooltip',
                                           'data-placement': 'right',
                                           'title': 'Prolele introduse trebuie să coincidă.'
                                           }),
                                help_text=_('Introduceți aceeași parolă.'))
    username = forms.EmailField(
        label=_('E-mail'),
        max_length=150,
        validators=[username_validator],
        error_messages={'unique': _("Un utilizator cu așa login deja există!")},
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Your e-mail',
                                      'data-toggle': 'tooltip',
                                      'data-placement': 'right',
                                      'title': 'Necesar. 150 de caracter sau mai puțin. '
                                               'Litere, cifre și doar următoarele simboluri @/./+/-/_.'
                                      })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2',)


def date_inserted_validator(date_inserted):
    if date_inserted > date.today():
        raise ValidationError('Date %(date)s cannot be from future!', params={'date': date_inserted},
                              code='future_date')


class DataIntroductionForm(models.ModelForm):
    quantity = forms.FloatField(
        label=_('Data înregistrării'),
        min_value=1.0,
        required=True,
        error_messages={
            'min_value': 'Valoarea masei nu poate fi mai mică egală cu 0(zero)!'
        },
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Cantitatea deșeurilor în kg',
                'data-toggle': 'tooltip',
                'data-placement': 'right',
                'title': 'Obligatoriu de introdus o valoare cel puțin 1(unu).'
            }
        )
    )
    waste_type = forms.IntegerField(
        required=True,
        min_value=0,
        max_value=3,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'data-toggle': 'tooltip',
                'data-placement': 'right',
                'title': 'Tipul deșeurilor este obligatoriu de specificat.'
            },
            choices=WasteType.choices
        ),
        label=_('Tip deșeuri'),
        error_messages={
            'min_value': 'Opțiune introduse este nevalidă',
            'max_value': 'Opțiune introduse este nevalidă'
        }
    )
    date_of_count = forms.DateField(
        label=_('Cantitate de deșeuri (kg)'),
        required=True,
        validators=[date_inserted_validator],
        error_messages={
            'future_date': 'Data introdusă nu poate fi din viitor!',
        },
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'data-toggle': 'tooltip',
                'data-placement': 'right',
                'title': 'Introduceți data când s-a înregistrat acestă cantitate, dacă este altă zi decât astăzi.'
            }
        ),
        initial=date.today()
    )

    class Meta:
        model = WasteData
        fields = ('quantity', 'waste_type', 'date_of_count')
        required = ('quantity', 'waste_type', 'date_of_count')
