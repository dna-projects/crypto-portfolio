from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, EmailInput, PasswordInput, TextInput, CharField
from .models import User
from .models import AssetEntry

# Add forms here
class UserRegistrationForm(UserCreationForm):
    password1 = CharField(
        label="Password",
        widget=PasswordInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-600', 
            'type': 'password', 
            'align': 'center',
            'autocomplete': 'new-password'
            }),
    )
    password2 = CharField(
        label="Confirm password",
        widget=PasswordInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-600', 
            'type': 'password', 
            'align': 'center',
            'autocomplete': 'new-password'
            }),
    )
    class Meta:
        # This will tie into Django's default user model
        # Has built-in fields: username, password1, pass2 (verification)
        model = User
        fields = ("username", "email")
        widgets = {
            'username': TextInput(attrs={ 
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-600'
                }),
            'email': EmailInput(attrs={ 
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-600'
                }),
        }

# New Token

class NewTokenForm(ModelForm):
    class Meta:
        model = AssetEntry
        fields = ("name", "cost_basis", "price_at_purchase", "quantity") #add entry_datetime

# BEFORE COMMIT

# Login Form

from django.contrib.auth.forms import AuthenticationForm

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username" , "password")
        widgets = {
            'username': TextInput(attrs={ 
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-600'
                }),
            'password': PasswordInput(attrs={ 
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-600'
                }),
        }