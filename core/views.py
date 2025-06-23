from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from .forms import UserRegistrationForm
from .decorators import citizen_required, volunteer_required, authority_required


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserRegistrationForm()
    return render(request, "registration/register.html", {"form": form})


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["role"] = self.request.user.role
        return context


# Example protected views
@citizen_required
def submit_report(request):
    # View only accessible to citizens
    return render(request, "core/submit_report.html")


@volunteer_required
def volunteer_dashboard(request):
    # View only accessible to volunteers
    return render(request, "core/volunteer_dashboard.html")


@authority_required
def manage_reports(request):
    # View only accessible to authorities
    return render(request, "core/manage_reports.html")
