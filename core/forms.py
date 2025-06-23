from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, DisasterReport


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
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class DisasterReportForm(forms.ModelForm):
    class Meta:
        model = DisasterReport
        fields = ["disaster_type", "description", "latitude", "longitude", "severity"]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Provide detailed information about the disaster...",
                }
            ),
            "latitude": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "any",
                    "placeholder": "Enter latitude (e.g., 3.140853)",
                }
            ),
            "longitude": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "any",
                    "placeholder": "Enter longitude (e.g., 101.693207)",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields:
            if field not in ["latitude", "longitude", "description"]:
                self.fields[field].widget.attrs.update({"class": "form-control"})

        # Add help texts
        self.fields["disaster_type"].help_text = "Select the type of disaster"
        self.fields["severity"].help_text = "Rate the severity of the disaster"
        self.fields["latitude"].help_text = "GPS latitude coordinate (-90 to 90)"
        self.fields["longitude"].help_text = "GPS longitude coordinate (-180 to 180)"

    def clean(self):
        cleaned_data = super().clean()
        lat = cleaned_data.get("latitude")
        lon = cleaned_data.get("longitude")

        if lat is not None and (lat < -90 or lat > 90):
            self.add_error("latitude", "Latitude must be between -90 and 90 degrees")

        if lon is not None and (lon < -180 or lon > 180):
            self.add_error(
                "longitude", "Longitude must be between -180 and 180 degrees"
            )

        return cleaned_data
