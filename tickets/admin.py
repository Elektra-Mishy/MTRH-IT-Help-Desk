from django.contrib import admin
from .models import Category, Ticket, Comment, TicketLog

admin.site.register(Category)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(TicketLog)
