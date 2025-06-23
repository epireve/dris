from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("register/", views.register, name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    # Disaster Report URLs
    path(
        "report/submit/", views.SubmitDisasterReportView.as_view(), name="submit_report"
    ),
    path("reports/", views.DisasterReportListView.as_view(), name="report_list"),
    path(
        "report/<int:pk>/", views.disaster_report_detail, name="disaster_report_detail"
    ),
    # Aid Request URLs
    path(
        "aid/submit/", views.SubmitAidRequestView.as_view(), name="submit_aid_request"
    ),
    path("aid/requests/", views.AidRequestListView.as_view(), name="aid_request_list"),
    path("aid/request/<int:pk>/", views.aid_request_detail, name="aid_request_detail"),
    # Volunteer Registration
    path("volunteer/register/", views.volunteer_register, name="volunteer_register"),
    # Authority Analytics
    path("authority/analytics/", views.authority_analytics, name="authority_analytics"),
    # Public Shelter Directory
    path("shelters/", views.shelter_directory, name="shelter_directory"),
    path("shelters/add/", views.shelter_add, name="shelter_add"),
    path("shelters/<int:pk>/edit/", views.shelter_edit, name="shelter_edit"),
]
