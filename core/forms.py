from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, DisasterReport, AidRequest, VolunteerProfile


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
        for field in self.fields:
            if field not in ["latitude", "longitude", "description"]:
                self.fields[field].widget.attrs.update({"class": "form-control"})

        self.fields["disaster_type"].help_text = "Select the type of disaster"
        self.fields["severity"].help_text = "Rate the severity of the disaster"
        self.fields["latitude"].help_text = "GPS latitude coordinate (-90 to 90)"
        self.fields["longitude"].help_text = "GPS longitude coordinate (-180 to 180)"


class AidRequestForm(forms.ModelForm):
    disaster_report = forms.ModelChoiceField(
        queryset=DisasterReport.objects.all(),
        required=False,
        empty_label="Select related disaster report (optional)",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = AidRequest
        fields = [
            "aid_type",
            "description",
            "quantity",
            "priority",
            "location_details",
            "disaster_report",
        ]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Describe what kind of aid you need...",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "How many items/people need assistance?",
                }
            ),
            "location_details": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Provide specific location details for aid delivery...",
                }
            ),
            "aid_type": forms.Select(attrs={"class": "form-control"}),
            "priority": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # If user is provided, filter disaster reports to show only user's reports
            self.fields["disaster_report"].queryset = DisasterReport.objects.filter(
                reporter=user
            )

        # Add help texts
        self.fields["aid_type"].help_text = "Select the type of aid needed"
        self.fields["quantity"].help_text = (
            "Enter the number of items/people (optional)"
        )
        self.fields["priority"].help_text = "How urgent is this request?"
        self.fields["disaster_report"].help_text = (
            "Link this request to a disaster report"
        )

    def clean(self):
        cleaned_data = super().clean()
        aid_type = cleaned_data.get("aid_type")
        description = cleaned_data.get("description")
        location_details = cleaned_data.get("location_details")

        if not description:
            self.add_error(
                "description", "Please provide a description of the aid needed"
            )

        if not location_details:
            self.add_error(
                "location_details", "Please provide location details for aid delivery"
            )

        return cleaned_data


# --- Volunteer Registration Form ---
class VolunteerRegistrationForm(forms.ModelForm):
    skills = forms.MultipleChoiceField(
        choices=VolunteerProfile.SKILL_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Select your skills",
    )
    preferred_locations = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "e.g. Selangor, Pahang"}),
        required=False,
        help_text="Comma-separated list of preferred volunteering locations",
    )

    class Meta:
        model = VolunteerProfile
        fields = [
            "skills",
            "availability",
            "preferred_locations",
            "contact_number",
            "emergency_contact",
            "notes",
        ]
        widgets = {
            "availability": forms.Select(attrs={"class": "form-control"}),
            "contact_number": forms.TextInput(attrs={"class": "form-control"}),
            "emergency_contact": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }

    def clean_preferred_locations(self):
        data = self.cleaned_data["preferred_locations"]
        # Convert comma-separated string to list
        return [loc.strip() for loc in data.split(",") if loc.strip()]
