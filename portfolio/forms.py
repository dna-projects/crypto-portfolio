from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User
from .models import AssetEntry

# Add forms here
class UserRegistrationForm(UserCreationForm):
    class Meta:
        # This will tie into Django's default user model
        # Has built-in fields: username, password1, pass2 (verification)
        model = User
        fields = ("username", "email", "password1", "password2")

# New Token

class NewTokenForm(ModelForm):
    class Meta:
        model = AssetEntry
        fields = ("name", "cost_basis", "price_at_purchase", "quantity") #add entry_datetime