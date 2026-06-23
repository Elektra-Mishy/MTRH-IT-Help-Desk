import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tickets.models import Ticket
from accounts.models import User
from departments.models import Department


@login_required
def dashboard(request):
    user = request.user

    if user.role == 'admin':
        total_tickets    = Ticket.objects.count()
        open_tickets     = Ticket.objects.filter(status__in=['pending', 'assigned', 'in_progress']).count()
        resolved_tickets = Ticket.objects.filter(status='resolved').count()
        critical_tickets = Ticket.objects.filter(priority='critical', status__in=['pending', 'assigned', 'in_progress']).count()
        total_users      = User.objects.count()
        recent_tickets   = Ticket.objects.select_related('department', 'category', 'assigned_to').order_by('-created_at')[:8]

        departments  = Department.objects.all()
        dept_labels  = json.dumps([d.department_name for d in departments])
        dept_counts  = json.dumps([Ticket.objects.filter(department=d).count() for d in departments])
        status_data  = json.dumps([
            Ticket.objects.filter(status='pending').count(),
            Ticket.objects.filter(status='assigned').count(),
            Ticket.objects.filter(status='in_progress').count(),
            Ticket.objects.filter(status='resolved').count(),
            Ticket.objects.filter(status='closed').count(),
        ])

        context = {
            'role': 'admin',
            'total_tickets': total_tickets,
            'open_tickets': open_tickets,
            'resolved_tickets': resolved_tickets,
            'critical_tickets': critical_tickets,
            'total_users': total_users,
            'recent_tickets': recent_tickets,
            'dept_labels': dept_labels,
            'dept_counts': dept_counts,
            'status_data': status_data,
        }

    elif user.role == 'technician':
        assigned    = Ticket.objects.filter(assigned_to=user)
        pending     = assigned.filter(status='assigned').count()
        in_prog     = assigned.filter(status='in_progress').count()
        resolved    = assigned.filter(status='resolved').count()
        recent      = assigned.order_by('-created_at')[:8]

        context = {
            'role': 'technician',
            'assigned_count': assigned.count(),
            'pending_count': pending,
            'in_progress_count': in_prog,
            'resolved_count': resolved,
            'recent_tickets': recent,
        }

    else:
        my_tickets  = Ticket.objects.filter(created_by=user)
        submitted   = my_tickets.count()
        resolved    = my_tickets.filter(status='resolved').count()
        pending     = my_tickets.filter(status='pending').count()
        recent      = my_tickets.order_by('-created_at')[:8]

        context = {
            'role': 'staff',
            'submitted': submitted,
            'resolved': resolved,
            'pending': pending,
            'recent_tickets': recent,
        }

    return render(request, 'dashboard/dashboard.html', context)