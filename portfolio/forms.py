from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import (
    ModelForm, 
    EmailInput, 
    PasswordInput, 
    TextInput, 
    CharField, 
    ChoiceField,
    NumberInput, 
    Select,
    HiddenInput)
from .models import User
from .models import AssetEntry

# Add forms here
class UserRegistrationForm(UserCreationForm):
    password1 = CharField(
        label="Password",
        widget=PasswordInput(attrs={
            'class': 'shadow rounded w-full py-2 px-3 text-white bg-[#01013D]/50 border border-[#6F7CF1] leading-tight',
            'type': 'password',
            'align': 'center',
            'autocomplete': 'new-password',
            'required': 'true',
            'minlength': 10
            }),
    )
    password2 = CharField(
        label="Confirm password",
        widget=PasswordInput(attrs={
            'class': 'shadow rounded w-full py-2 px-3 text-white bg-[#01013D]/50 border border-[#6F7CF1] leading-tight',
            'type': 'password',
            'align': 'center',
            'autocomplete': 'new-password',
            'required': 'true',
            'minlength': 10
            }),
    )
    class Meta:
        # This will tie into Django's default user model
        # Has built-in fields: username, password1, pass2 (verification)
        model = User
        fields = ("username", "email")
        widgets = {
            'username': TextInput(attrs={
                'class': 'shadow rounded w-full py-2 px-3 text-white bg-[#01013D]/50 border border-[#6F7CF1] leading-tight'
                }),
            'email': EmailInput(attrs={
                'class': 'shadow rounded w-full py-2 px-3 text-white bg-[#01013D]/50 border border-[#6F7CF1] leading-tight'
                }),
        }

# Login Form
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'shadow rounded w-full py-2 px-3 text-white bg-[#01013D]/50 border border-[#6F7CF1] leading-tight'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'shadow rounded w-full py-2 px-3 text-white bg-[#01013D]/50 border border-[#6F7CF1] leading-tight'}
        )

# New Token
class NewTokenForm(ModelForm):
    def updateChoices(self, token_names):
        # Create a choices list that consists of a value equal to name and a label
        # equal to name -> ('Bitcoin', 'Bitcoin')
        self.token_names = [(name, name) for name in [*token_names]]

        # Add placeholder to the beginning of the option list
        self.token_names.insert(0, ('', '-- Select token --'))

        self.fields['name'].widget = \
            Select(
                choices=(self.token_names),
                attrs={
                    'class': 'shadow w-full text-white bg-[#01013D]/70 border border-[#6F7CF1] leading-tight text-sm rounded-lg block p-2.5'
                })

    class Meta:
        model = AssetEntry
        fields = ("name", "cost_basis", "price_at_purchase", "quantity", "coingecko_id") #add entry_datetime
        widgets = {
            'cost_basis': NumberInput(attrs={
                'class': 'shadow w-full text-white bg-[#01013D]/70 border border-[#6F7CF1] leading-tight text-sm rounded-lg block pl-6 py-2.5 pr-2.5',
                'min': '0'
            }),
            'quantity': NumberInput(attrs={
                'class': 'shadow w-full text-white bg-[#01013D]/70 border border-[#6F7CF1] leading-tight text-sm rounded-lg block p-2.5',
                'min': '0'
            }),
            'price_at_purchase': NumberInput(attrs={
                'class': 'shadow w-full text-white bg-[#01013D]/70 border border-[#6F7CF1] leading-tight text-sm rounded-lg block pl-6 py-2.5 pr-2.5',
                'min': '0'
            }),
            'coingecko_id': HiddenInput
        }

# Edit existing token. Uses the new token form and excludes the unnecessary fields
class EditTokenForm(NewTokenForm):
    class Meta(NewTokenForm.Meta):
        exclude = ["name", "coingecko_id"]
