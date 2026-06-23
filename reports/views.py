from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
import csv
from tickets.models import Ticket
from accounts.models import User
from departments.models import Department


@login_required
def reports(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return render(request, 'reports/reports.html', {})

    # department report
    departments = Department.objects.all()
    dept_report = []
    for dept in departments:
        count    = Ticket.objects.filter(department=dept).count()
        resolved = Ticket.objects.filter(department=dept, status='resolved').count()
        pending  = Ticket.objects.filter(department=dept, status='pending').count()
        dept_report.append({
            'name': dept.department_name,
            'total': count,
            'resolved': resolved,
            'pending': pending,
        })

    # technician report
    technicians = User.objects.filter(role__in=['technician', 'admin'])
    tech_report = []
    for tech in technicians:
        resolved    = Ticket.objects.filter(assigned_to=tech, status='resolved').count()
        in_progress = Ticket.objects.filter(assigned_to=tech, status='in_progress').count()
        assigned    = Ticket.objects.filter(assigned_to=tech).count()
        tech_report.append({
            'name': tech.get_full_name() or tech.username,
            'assigned': assigned,
            'resolved': resolved,
            'in_progress': in_progress,
        })

    # status report
    status_report = {
        'pending':     Ticket.objects.filter(status='pending').count(),
        'assigned':    Ticket.objects.filter(status='assigned').count(),
        'in_progress': Ticket.objects.filter(status='in_progress').count(),
        'resolved':    Ticket.objects.filter(status='resolved').count(),
        'closed':      Ticket.objects.filter(status='closed').count(),
        'total':       Ticket.objects.count(),
    }

    # all tickets
    all_tickets = Ticket.objects.select_related(
        'department', 'category', 'assigned_to', 'created_by'
    ).order_by('-created_at')

    context = {
        'dept_report': dept_report,
        'tech_report': tech_report,
        'status_report': status_report,
        'all_tickets': all_tickets,
    }
    return render(request, 'reports/reports.html', context)


@login_required
def export_csv(request):
    if request.user.role != 'admin':
        return HttpResponse('Access denied', status=403)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mtrh_tickets_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Ticket Number', 'Title', 'Category', 'Department',
        'Priority', 'Status', 'Created By', 'Assigned To', 'Date Created'
    ])

    tickets = Ticket.objects.select_related(
        'category', 'department', 'created_by', 'assigned_to'
    ).all()

    for ticket in tickets:
        writer.writerow([
            ticket.ticket_number,
            ticket.title,
            ticket.category.category_name if ticket.category else '',
            ticket.department.department_name if ticket.department else '',
            ticket.get_priority_display(),
            ticket.get_status_display(),
            ticket.created_by.get_full_name() if ticket.created_by else '',
            ticket.assigned_to.get_full_name() if ticket.assigned_to else 'Unassigned',
            ticket.created_at.strftime('%d %b %Y %H:%M'),
        ])

    return response


@login_required
def export_pdf(request):
    if request.user.role != 'admin':
        return HttpResponse('Access denied', status=403)

    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm
    import io

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    elements = []

    title = Paragraph("<b>MTRH IT Help Desk — Ticket Report</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph("<b>Status Summary</b>", styles['Heading2']))
    elements.append(Spacer(1, 0.3*cm))

    status_data = [
        ['Status', 'Count'],
        ['Pending',     str(Ticket.objects.filter(status='pending').count())],
        ['Assigned',    str(Ticket.objects.filter(status='assigned').count())],
        ['In Progress', str(Ticket.objects.filter(status='in_progress').count())],
        ['Resolved',    str(Ticket.objects.filter(status='resolved').count())],
        ['Closed',      str(Ticket.objects.filter(status='closed').count())],
        ['TOTAL',       str(Ticket.objects.count())],
    ]

    t = Table(status_data, colWidths=[10*cm, 5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F6E56')),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F0F4F8')]),
        ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING',    (0,0), (-1,-1), 8),
        ('FONTNAME',   (0,-1), (-1,-1), 'Helvetica-Bold'),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 0.8*cm))

    elements.append(Paragraph("<b>All Tickets</b>", styles['Heading2']))
    elements.append(Spacer(1, 0.3*cm))

    ticket_data = [['Ticket #', 'Title', 'Department', 'Priority', 'Status', 'Assigned To']]
    tickets = Ticket.objects.select_related('department', 'assigned_to').all()
    for ticket in tickets:
        ticket_data.append([
            ticket.ticket_number,
            ticket.title[:35],
            str(ticket.department) if ticket.department else '',
            ticket.get_priority_display(),
            ticket.get_status_display(),
            ticket.assigned_to.get_full_name() if ticket.assigned_to else 'Unassigned',
        ])

    t2 = Table(ticket_data, colWidths=[2.5*cm, 5.5*cm, 3*cm, 2*cm, 2.5*cm, 3*cm])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F6E56')),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F0F4F8')]),
        ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING',    (0,0), (-1,-1), 6),
    ]))
    elements.append(t2)

    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mtrh_tickets_report.pdf"'
    return response