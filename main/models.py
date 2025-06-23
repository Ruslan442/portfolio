from datetime import date, timedelta
from django.db import models
from django.contrib import admin
from simple_history.models import HistoricalRecords


class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    course = models.IntegerField()
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Projects(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateField()
    history = HistoricalRecords()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class ParticipationInProjects(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    new_date = models.DateField()

    def __str__(self):
        return f"{self.student} - {self.project}"

    class Meta:
        verbose_name = 'Участие в проекте'
        verbose_name_plural = 'Участии в проекте'


class Events(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    history = HistoricalRecords()

    @admin.display(
        boolean=True,
        ordering="date",
        description="Событие прошло недавно?",
    )
    def was_held_recently(self):
        today = date.today()
        difference = today - self.date
        return difference <= timedelta(days=30)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


class ParticipationInEvents(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    participation_date = models.DateField()

    def __str__(self):
        return f"{self.student} - {self.event}"

    class Meta:
        verbose_name = 'Участие в событии'
        verbose_name_plural = 'Участия в событии'


class ParticipationResults(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(Events, on_delete=models.CASCADE, null=True)
    grade = models.IntegerField()

    def __str__(self):
        return f"{self.student} - {self.project} - {self.event}"

    class Meta:
        verbose_name = 'Результат выступления'
        verbose_name_plural = 'Результаты выступления'
