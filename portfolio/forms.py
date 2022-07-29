from django.contrib.auth.forms import UserCreationForm
from .models import User

# Add forms here
class UserRegistrationForm(UserCreationForm):
    class Meta:
        # This will tie into Django's default user model
        # Has built-in fields: username, password1, pass2 (verification)
        model = User
        fields = ("username", "email", "password1", "password2")