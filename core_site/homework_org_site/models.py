from django.contrib.auth.models import User
from django.db import models
from django.db.models import ManyToManyField


class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher",
    )
    bio = models.CharField(max_length=200)
    subjects = ManyToManyField('Subject')

    def __str__(self):
        return self.user.username

class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student",
    )
    school_year = models.IntegerField()
    notes = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    subject = models.ForeignKey(
        'Subject',
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    date = models.DateField()
    duration = models.IntegerField(default=45)
    topic = models.CharField(max_length=200)

    def __str__(self):
        return self.subject.name + ' ' + self.teacher.user.username

class HomeworkStatus(models.TextChoices):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class Homework(models.Model):
    student = models.ForeignKey(
        'Student',
            on_delete=models.CASCADE,
            related_name='homeworks'
    )
    subject = models.ForeignKey(
        'Subject',
            on_delete=models.CASCADE,
            related_name='homeworks'
    )
    status = models.CharField(
        max_length=200,
        choices=HomeworkStatus.choices,
        default=HomeworkStatus.TODO,
        blank=True
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    due_date = models.DateField()
