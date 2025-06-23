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
    # Role-protected URLs
    path("report/submit/", views.submit_report, name="submit_report"),
    path("volunteer/dashboard/", views.volunteer_dashboard, name="volunteer_dashboard"),
    path("authority/reports/", views.manage_reports, name="manage_reports"),
]
