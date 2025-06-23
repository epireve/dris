from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, ListView, CreateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import (
    UserRegistrationForm,
    DisasterReportForm,
    AidRequestForm,
    VolunteerRegistrationForm,
)
from .models import DisasterReport, AidRequest, VolunteerProfile, User, TaskAssignment
from .decorators import citizen_required, volunteer_required, authority_required


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


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return reverse_lazy("admin:index")
        return reverse_lazy("home")


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
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return queryset
        if user.role == "CITIZEN":
            return queryset.filter(reporter=user)
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
        if user.is_superuser or user.is_staff:
            return queryset
        if user.role == "CITIZEN":
            return queryset.filter(requester=user)
        elif user.role == "VOLUNTEER":
            return queryset.filter(status__in=["PENDING", "APPROVED", "IN_PROGRESS"])
        return queryset


@login_required
def aid_request_detail(request, pk):
    aid_request = get_object_or_404(AidRequest, pk=pk)
    assignments = TaskAssignment.objects.filter(aid_request=aid_request).select_related(
        "volunteer", "authority"
    )
    can_assign = request.user.is_authenticated and (
        request.user.role == "AUTHORITY"
        or request.user.is_superuser
        or request.user.is_staff
    )
    volunteers = User.objects.filter(role="VOLUNTEER", is_active=True)
    assignment_error = None

    # Assignment form handling
    if can_assign and request.method == "POST" and "assign_volunteer" in request.POST:
        volunteer_id = request.POST.get("volunteer_id")
        notes = request.POST.get("assignment_notes", "")
        try:
            volunteer = User.objects.get(pk=volunteer_id, role="VOLUNTEER")
            TaskAssignment.objects.create(
                authority=request.user,
                volunteer=volunteer,
                aid_request=aid_request,
                notes=notes,
                status="ASSIGNED",
            )
            messages.success(
                request, f"Volunteer {volunteer.username} assigned successfully."
            )
            return redirect("aid_request_detail", pk=pk)
        except Exception as e:
            assignment_error = str(e)
            messages.error(request, f"Assignment failed: {assignment_error}")

    context = {
        "aid_request": aid_request,
        "can_update": request.user.role in ["VOLUNTEER", "AUTHORITY"],
        "assignments": assignments,
        "can_assign": can_assign,
        "volunteers": volunteers,
        "assignment_error": assignment_error,
    }
    return render(request, "aid/request_detail.html", context)


def volunteer_register(request):
    if not request.user.is_authenticated or request.user.role != "VOLUNTEER":
        messages.error(
            request, "You must be logged in as a volunteer to register your profile."
        )
        return redirect("login")
    try:
        profile = request.user.volunteer_profile
        is_update = True
    except VolunteerProfile.DoesNotExist:
        profile = None
        is_update = False

    if request.method == "POST":
        form = VolunteerRegistrationForm(request.POST, instance=profile)
        if form.is_valid():
            volunteer_profile = form.save(commit=False)
            volunteer_profile.user = request.user
            volunteer_profile.save()
            form.save_m2m()
            messages.success(request, "Volunteer profile saved successfully.")
            return redirect("home")
    else:
        form = VolunteerRegistrationForm(instance=profile)

    return render(
        request, "volunteer/register.html", {"form": form, "is_update": is_update}
    )
