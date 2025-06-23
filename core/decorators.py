from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from functools import wraps


def role_required(allowed_roles):
    """
    Decorator for views that checks that the user has the required role.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            if request.user.role not in (
                allowed_roles
                if isinstance(allowed_roles, (list, tuple))
                else [allowed_roles]
            ):
                return redirect("home")
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


citizen_required = role_required("CITIZEN")
volunteer_required = role_required("VOLUNTEER")
authority_required = role_required("AUTHORITY")
