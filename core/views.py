from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from django.utils.decorators import method_decorator
from .forms import UserRegistrationForm, DisasterReportForm
from .models import DisasterReport
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


@method_decorator(citizen_required, name="dispatch")
class SubmitDisasterReportView(TemplateView):
    template_name = "disaster/submit_report.html"

    def get(self, request, *args, **kwargs):
        form = DisasterReportForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = DisasterReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.save()
            return redirect("disaster_report_detail", pk=report.pk)
        return render(request, self.template_name, {"form": form})


@method_decorator(login_required, name="dispatch")
class DisasterReportListView(ListView):
    model = DisasterReport
    template_name = "disaster/report_list.html"
    context_object_name = "reports"
    ordering = ["-timestamp"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == "CITIZEN":
            return queryset.filter(reporter=self.request.user)
        return queryset


@login_required
def disaster_report_detail(request, pk):
    report = DisasterReport.objects.get(pk=pk)
    return render(request, "disaster/report_detail.html", {"report": report})
