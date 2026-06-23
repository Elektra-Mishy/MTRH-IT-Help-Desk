from django.db import models
from django.conf import settings


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ['category_name']
        verbose_name_plural = 'Categories'


class Ticket(models.Model):

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )

    ticket_number   = models.CharField(max_length=20, unique=True, editable=False)
    title           = models.CharField(max_length=200)
    description     = models.TextField()
    priority        = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    department      = models.ForeignKey(
                          'departments.Department',
                          on_delete=models.SET_NULL,
                          null=True
                      )
    category        = models.ForeignKey(
                          Category,
                          on_delete=models.SET_NULL,
                          null=True
                      )
    created_by      = models.ForeignKey(
                          settings.AUTH_USER_MODEL,
                          on_delete=models.CASCADE,
                          related_name='created_tickets'
                      )
    assigned_to     = models.ForeignKey(
                          settings.AUTH_USER_MODEL,
                          on_delete=models.SET_NULL,
                          null=True,
                          blank=True,
                          related_name='assigned_tickets'
                      )
    attachment      = models.ImageField(upload_to='ticket_attachments/', null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ticket_number} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            last = Ticket.objects.order_by('id').last()
            next_id = (last.id + 1) if last else 1
            self.ticket_number = f"TKT-{next_id:04d}"
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    ticket     = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.ticket.ticket_number}"

    class Meta:
        ordering = ['created_at']


class TicketLog(models.Model):
    ticket      = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='logs')
    changed_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    old_status  = models.CharField(max_length=20, blank=True)
    new_status  = models.CharField(max_length=20, blank=True)
    note        = models.CharField(max_length=255, blank=True)
    changed_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket.ticket_number} | {self.old_status} → {self.new_status}"

    class Meta:
        ordering = ['changed_at']
