from django.utils import timezone
from rest_framework import serializers
from .models import Student, Projects, ParticipationInProjects, Events, ParticipationInEvents, ParticipationResults


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def validate_date_of_birth(self, value):
        # Дата рождения не должна быть в будущем
        if value > timezone.now().date():
            raise serializers.ValidationError("Дата рождения не может быть в будущем.")
        return value


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'

    def validate_creation_date(self, value):
        # Дата создания проекта не должна быть в будущем
        if value > timezone.now().date():
            raise serializers.ValidationError("Дата создания проекта не может быть в будущем.")
        return value


class ParticipationInProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipationInProjects
        fields = '__all__'
        read_only_fields = ('project',)

    def validate(self, data):
        # Дата начала не должна быть позже даты окончания
        start_date = data['start_date']
        end_date = data['end_date']
        if start_date > end_date:
            raise serializers.ValidationError("Дата начала не может быть позже даты окончания.")
        return data


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'

    def validate_date(self, value):
        # Дата события не должна быть в будущем
        if value > timezone.now().date():
            raise serializers.ValidationError("Дата события не может быть в будущем.")
        return value


class ParticipationInEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipationInEvents
        fields = '__all__'


class ParticipationResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipationResults
        fields = '__all__'
        read_only_fields = ('student',)

    def validate_grade(self, value):
        # Оценка должна быть в пределах от 1 до 10
        if not 1 <= value <= 10:
            raise serializers.ValidationError("Оценка должна быть в пределах от 1 до 10.")
        return value
