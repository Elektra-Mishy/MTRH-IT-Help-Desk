from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        messages.error(request, 'You do not have permission to access that page.')
        return redirect('dashboard')
    return wrapper


def technician_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role in ['admin', 'technician']:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'You do not have permission to access that page.')
        return redirect('dashboard')
    return wrapper