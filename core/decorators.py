from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Please login to access this page.")
                return redirect("login")

            if request.user.role != role:
                messages.error(
                    request,
                    f"Access denied. This page is only accessible to {role.lower()} users.",
                )
                return redirect("home")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def citizen_required(view_func):
    return role_required("CITIZEN")(view_func)


def volunteer_required(view_func):
    return role_required("VOLUNTEER")(view_func)


def authority_required(view_func):
    return role_required("AUTHORITY")(view_func)
