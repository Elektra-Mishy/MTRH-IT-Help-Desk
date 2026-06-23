from django.core.mail import send_mail
from django.conf import settings


def send_ticket_assigned_email(ticket, technician):
    subject = f'[MTRH Help Desk] Ticket {ticket.ticket_number} Assigned to You'

    message = f"""
Dear {technician.get_full_name()},

A support ticket has been assigned to you on the MTRH IT Help Desk system.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TICKET DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ticket Number : {ticket.ticket_number}
Title         : {ticket.title}
Category      : {ticket.category}
Department    : {ticket.department}
Priority      : {ticket.get_priority_display()}
Status        : {ticket.get_status_display()}
Submitted by  : {ticket.created_by.get_full_name()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DESCRIPTION:
{ticket.description}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Please log in to the MTRH IT Help Desk system to view and resolve this ticket.

This is an automated message from MTRH IT Help Desk.
Do not reply to this email.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MTRH ICT Department
Moi Teaching & Referral Hospital
"""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[technician.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


def send_ticket_created_email(ticket):
    subject = f'[MTRH Help Desk] Your Ticket {ticket.ticket_number} Has Been Received'

    message = f"""
Dear {ticket.created_by.get_full_name()},

Your support ticket has been successfully submitted to the MTRH IT Help Desk.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TICKET DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ticket Number : {ticket.ticket_number}
Title         : {ticket.title}
Category      : {ticket.category}
Department    : {ticket.department}
Priority      : {ticket.get_priority_display()}
Status        : Pending
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your ticket will be reviewed and assigned to a technician shortly.
You will receive another email when it is assigned.

This is an automated message from MTRH IT Help Desk.
Do not reply to this email.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MTRH ICT Department
Moi Teaching & Referral Hospital
"""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[ticket.created_by.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


def send_ticket_resolved_email(ticket):
    subject = f'[MTRH Help Desk] Your Ticket {ticket.ticket_number} Has Been Resolved'

    message = f"""
Dear {ticket.created_by.get_full_name()},

We are pleased to inform you that your support ticket has been resolved.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TICKET DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ticket Number : {ticket.ticket_number}
Title         : {ticket.title}
Resolved by   : {ticket.assigned_to.get_full_name() if ticket.assigned_to else 'ICT Team'}
Status        : Resolved
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If the issue persists, please log in to the MTRH IT Help Desk
and add a comment to your ticket or create a new one.

This is an automated message from MTRH IT Help Desk.
Do not reply to this email.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MTRH ICT Department
Moi Teaching & Referral Hospital
"""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[ticket.created_by.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False