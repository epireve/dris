from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("register/", views.register, name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    # Disaster Report URLs
    path(
        "report/submit/", views.SubmitDisasterReportView.as_view(), name="submit_report"
    ),
    path("reports/", views.DisasterReportListView.as_view(), name="report_list"),
    path(
        "report/<int:pk>/", views.disaster_report_detail, name="disaster_report_detail"
    ),
]
