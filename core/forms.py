from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=True,
        help_text="Select your role in the system",
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        # Add Bootstrap classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
