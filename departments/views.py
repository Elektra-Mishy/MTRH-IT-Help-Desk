from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Department
from tickets.models import Ticket


@login_required
def department_list(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    departments = Department.objects.all()
    dept_data = []
    for dept in departments:
        total    = Ticket.objects.filter(department=dept).count()
        open_t   = Ticket.objects.filter(department=dept, status__in=['pending','assigned','in_progress']).count()
        resolved = Ticket.objects.filter(department=dept, status='resolved').count()
        dept_data.append({
            'dept': dept,
            'total': total,
            'open': open_t,
            'resolved': resolved,
        })
    return render(request, 'departments/department_list.html', {'dept_data': dept_data})


@login_required
def department_create(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    if request.method == 'POST':
        name = request.POST.get('department_name', '').strip()
        if name:
            if Department.objects.filter(department_name=name).exists():
                messages.error(request, 'Department already exists.')
            else:
                Department.objects.create(department_name=name)
                messages.success(request, f'Department "{name}" created.')
                return redirect('department_list')
    return render(request, 'departments/department_form.html', {'action': 'Create'})


@login_required
def department_edit(request, pk):
    if request.user.role != 'admin':
        return redirect('dashboard')
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('department_name', '').strip()
        if name:
            dept.department_name = name
            dept.save()
            messages.success(request, 'Department updated.')
            return redirect('department_list')
    return render(request, 'departments/department_form.html', {
        'action': 'Edit', 'dept': dept
    })


@login_required
def department_delete(request, pk):
    if request.user.role != 'admin':
        return redirect('dashboard')
    dept = get_object_or_404(Department, pk=pk)
    dept.delete()
    messages.success(request, 'Department deleted.')
    return redirect('department_list')