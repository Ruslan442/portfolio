from django.core.management.base import BaseCommand
from datetime import datetime
from main.models import Student


class Command(BaseCommand):
    help = 'Вычислить средний возраст студентов'

    def handle(self, *args, **options):
        students = Student.objects.all()

        if not students:
            self.stdout.write(self.style.WARNING('Нет студентов в базе данных.'))
            return

        today = datetime.today()
        total_age = 0
        total_students = 0

        for student in students:
            date_of_birth = student.date_of_birth
            age = today.year - date_of_birth.year - (
                    (today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            total_age += age
            total_students += 1

        average_age = total_age / total_students if total_students > 0 else 0

        self.stdout.write(self.style.SUCCESS(f'Средний возраст студентов: {average_age:.2f} лет'))
