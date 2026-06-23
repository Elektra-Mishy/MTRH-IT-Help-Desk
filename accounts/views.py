from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from departments.models import Department


def redirect_home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'accounts/login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def user_list(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    users = User.objects.all().order_by('role', 'first_name')
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
def user_create(request):
    if request.user.role != 'admin':
        return redirect('dashboard')

    departments = Department.objects.all()

    if request.method == 'POST':
        username    = request.POST.get('username', '').strip()
        first_name  = request.POST.get('first_name', '').strip()
        last_name   = request.POST.get('last_name', '').strip()
        email       = request.POST.get('email', '').strip()
        role        = request.POST.get('role', 'staff')
        dept_id     = request.POST.get('department', '')
        password    = request.POST.get('password', '').strip()

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role,
            )
            if dept_id:
                user.department_id = dept_id
                user.save()
            messages.success(request, f'User {first_name} {last_name} created successfully.')
            return redirect('user_list')

    return render(request, 'accounts/user_create.html', {'departments': departments})


@login_required
def user_edit(request, pk):
    if request.user.role != 'admin':
        return redirect('dashboard')

    user = get_object_or_404(User, pk=pk)
    departments = Department.objects.all()

    if request.method == 'POST':
        user.first_name   = request.POST.get('first_name', '').strip()
        user.last_name    = request.POST.get('last_name', '').strip()
        user.email        = request.POST.get('email', '').strip()
        user.role         = request.POST.get('role', 'staff')
        dept_id           = request.POST.get('department', '')
        user.department_id = dept_id if dept_id else None
        user.save()
        messages.success(request, 'User updated successfully.')
        return redirect('user_list')

    return render(request, 'accounts/user_edit.html', {
        'edit_user': user,
        'departments': departments
    })


@login_required
def user_delete(request, pk):
    if request.user.role != 'admin':
        return redirect('dashboard')
    user = get_object_or_404(User, pk=pk)
    if user != request.user:
        user.delete()
        messages.success(request, 'User deleted.')
    else:
        messages.error(request, 'You cannot delete your own account.')
    return redirect('user_list')