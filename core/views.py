from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, CreateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegistrationForm, DisasterReportForm, AidRequestForm
from .models import DisasterReport, AidRequest
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
            if self.request.user.role == "CITIZEN":
                context["disaster_reports"] = DisasterReport.objects.filter(
                    reporter=self.request.user
                ).order_by("-timestamp")[:5]
                context["aid_requests"] = AidRequest.objects.filter(
                    requester=self.request.user
                ).order_by("-timestamp")[:5]
        return context


@method_decorator(citizen_required, name="dispatch")
class SubmitDisasterReportView(CreateView):
    template_name = "disaster/submit_report.html"
    form_class = DisasterReportForm
    success_url = reverse_lazy("report_list")

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Disaster report submitted successfully.")
        return response


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
    report = get_object_or_404(DisasterReport, pk=pk)
    if request.user.role == "CITIZEN" and report.reporter != request.user:
        return redirect("home")
    return render(request, "disaster/report_detail.html", {"report": report})


@method_decorator(citizen_required, name="dispatch")
class SubmitAidRequestView(CreateView):
    template_name = "aid/submit_request.html"
    form_class = AidRequestForm
    success_url = reverse_lazy("aid_request_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user

        # Pre-select disaster report if provided in URL
        disaster_report_id = self.request.GET.get("disaster_report")
        if disaster_report_id:
            try:
                disaster_report = DisasterReport.objects.get(
                    id=disaster_report_id, reporter=self.request.user
                )
                initial = kwargs.get("initial", {})
                initial["disaster_report"] = disaster_report
                kwargs["initial"] = initial
            except DisasterReport.DoesNotExist:
                pass

        return kwargs

    def form_valid(self, form):
        form.instance.requester = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Aid request submitted successfully.")

        # If this aid request is linked to a disaster report, redirect to that report
        if form.instance.disaster_report:
            self.success_url = reverse_lazy(
                "disaster_report_detail",
                kwargs={"pk": form.instance.disaster_report.pk},
            )

        return response


@method_decorator(login_required, name="dispatch")
class AidRequestListView(ListView):
    model = AidRequest
    template_name = "aid/request_list.html"
    context_object_name = "requests"
    ordering = ["-timestamp"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.role == "CITIZEN":
            return queryset.filter(requester=user)
        elif user.role == "VOLUNTEER":
            return queryset.filter(status__in=["PENDING", "APPROVED", "IN_PROGRESS"])
        return queryset  # Authorities can see all


@login_required
def aid_request_detail(request, pk):
    aid_request = get_object_or_404(AidRequest, pk=pk)

    # Check permissions
    if request.user.role == "CITIZEN" and aid_request.requester != request.user:
        messages.error(request, "You do not have permission to view this aid request.")
        return redirect("aid_request_list")

    # Handle status updates from volunteers and authorities
    if request.method == "POST" and request.user.role in ["VOLUNTEER", "AUTHORITY"]:
        new_status = request.POST.get("status")
        notes = request.POST.get("notes")

        if new_status and new_status in dict(AidRequest.STATUS_CHOICES):
            aid_request.status = new_status
            if notes:
                aid_request.notes = (
                    aid_request.notes + "\n\n" if aid_request.notes else ""
                ) + notes
            aid_request.assigned_to = request.user
            aid_request.save()
            messages.success(request, "Aid request status updated successfully.")
            return redirect("aid_request_detail", pk=pk)

    context = {
        "aid_request": aid_request,
        "can_update": request.user.role in ["VOLUNTEER", "AUTHORITY"],
    }

    return render(request, "aid/request_detail.html", context)
