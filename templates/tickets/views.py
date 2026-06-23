from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from tickets.models import Ticket, TicketLog, Category
from departments.models import Department
from tickets.forms import CommentForm, TicketAssignForm


@login_required
def ticket_list(request):
    user = request.user
    tickets = Ticket.objects.all()

    if user.role == 'technician':
        tickets = tickets.filter(assigned_to=user)
    elif user.role == 'staff':
        tickets = tickets.filter(created_by=user)

    q = request.GET.get('q', '')
    if q:
        tickets = tickets.filter(
            Q(ticket_number__icontains=q) |
            Q(title__icontains=q) |
            Q(department__department_name__icontains=q)
        )

    status = request.GET.get('status', '')
    if status:
        tickets = tickets.filter(status=status)

    priority = request.GET.get('priority', '')
    if priority:
        tickets = tickets.filter(priority=priority)

    context = {
        'tickets': tickets,
        'q': q,
        'status': status,
        'priority': priority,
    }
    return render(request, 'tickets/ticket_list.html', context)


@login_required
def ticket_create(request):
    categories = Category.objects.all()
    departments = Department.objects.all()

    print("CATEGORIES COUNT:", categories.count())
    print("DEPARTMENTS COUNT:", departments.count())

    if request.method == 'POST':
        title       = request.POST.get('title', '').strip()
        category_id = request.POST.get('category', '')
        dept_id     = request.POST.get('department', '')
        priority    = request.POST.get('priority', '')
        description = request.POST.get('description', '').strip()
        attachment  = request.FILES.get('attachment')

        if title and category_id and dept_id and priority and description:
            ticket = Ticket(
                title=title,
                category_id=category_id,
                department_id=dept_id,
                priority=priority,
                description=description,
                created_by=request.user,
                status='pending'
            )
            if attachment:
                ticket.attachment = attachment
            ticket.save()

            TicketLog.objects.create(
                ticket=ticket,
                changed_by=request.user,
                old_status='',
                new_status='pending',
                note='Ticket created'
            )
            messages.success(request, f'Ticket {ticket.ticket_number} created successfully.')
            return redirect('ticket_detail', pk=ticket.pk)
        else:
            messages.error(request, 'Please fill in all required fields.')

    context = {
        'categories': categories,
        'departments': departments,
    }
    return render(request, 'tickets/ticket_create.html', context)


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    comments = ticket.comments.all()
    logs = ticket.logs.all()
    comment_form = CommentForm()
    assign_form = TicketAssignForm(instance=ticket)

    if request.method == 'POST':

        if 'add_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.ticket = ticket
                comment.user = request.user
                comment.save()
                messages.success(request, 'Comment added.')
                return redirect('ticket_detail', pk=pk)

        elif 'update_ticket' in request.POST:
            old_status = ticket.status
            assign_form = TicketAssignForm(request.POST, instance=ticket)
            if assign_form.is_valid():
                updated = assign_form.save(commit=False)
                if updated.assigned_to and updated.status == 'pending':
                    updated.status = 'assigned'
                updated.save()
                if old_status != updated.status:
                    TicketLog.objects.create(
                        ticket=ticket,
                        changed_by=request.user,
                        old_status=old_status,
                        new_status=updated.status,
                        note=f'Status updated by {request.user.get_full_name()}'
                    )
                messages.success(request, 'Ticket updated successfully.')
                return redirect('ticket_detail', pk=pk)

    context = {
        'ticket': ticket,
        'comments': comments,
        'logs': logs,
        'comment_form': comment_form,
        'assign_form': assign_form,
    }
    return render(request, 'tickets/ticket_detail.html', context)


@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    return render(request, 'tickets/my_tickets.html', {'tickets': tickets})


@login_required
def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.user.role == 'admin':
        ticket.delete()
        messages.success(request, 'Ticket deleted.')
    return redirect('ticket_list')