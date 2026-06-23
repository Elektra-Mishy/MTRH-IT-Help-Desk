from django.core.management.base import BaseCommand
from departments.models import Department
from tickets.models import Category


class Command(BaseCommand):
    help = 'Seed departments and categories'

    def handle(self, *args, **kwargs):

        departments = [
            'Administration',
            'ICT Department',
            'Health Records',
            'Finance',
            'Human Resource',
            'Laboratory',
            'Pharmacy',
            'Radiology',
            'Emergency Department',
            'Medical Wards',
        ]

        for name in departments:
            obj, created = Department.objects.get_or_create(department_name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created department: {name}'))
            else:
                self.stdout.write(f'  Already exists: {name}')

        categories = [
            'Printer Issue',
            'Network Issue',
            'Computer Issue',
            'Internet Problem',
            'Email Problem',
            'Software Error',
            'Hardware Failure',
            'Telephone Issue',
            'Account Access',
            'Other',
        ]

        for name in categories:
            obj, created = Category.objects.get_or_create(category_name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created category: {name}'))
            else:
                self.stdout.write(f'  Already exists: {name}')

        self.stdout.write(self.style.SUCCESS('\nSeed complete!'))