from django import forms
from tickets.models import Ticket, Comment


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'category', 'department', 'priority', 'description', 'attachment']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. HP Printer Not Printing in Lab'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the issue in detail — what happened, when, and how many users are affected...',
                'rows': 4
            }),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add a comment...',
                'rows': 2
            })
        }


class TicketAssignForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['assigned_to', 'status']
        widgets = {
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from accounts.models import User
        self.fields['assigned_to'].queryset = User.objects.filter(
            role__in=['technician', 'admin']
        )
        self.fields['assigned_to'].empty_label = 'Unassigned'