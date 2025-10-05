from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from homework_org_site.models import Lesson, Subject, Student


class LessonAddForm(forms.ModelForm):

    student = forms.ModelChoiceField(
        queryset=Student.objects.none(),
        label="Student",
        empty_label="Select a student"
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(),
        label="Subject",
        empty_label="Select a subject"
    )

    class Meta:
        model = Lesson
        fields = ['student', 'subject', 'date', 'duration', 'topic']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'duration': forms.NumberInput(attrs={'min': 15, 'step': 15}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].queryset = Subject.objects.all().order_by("name")
        self.fields["student"].queryset = (
            Student.objects.select_related("user")
            .order_by("user__last_name", "user__first_name", "user__username")
        )
        self.fields["student"].label_from_instance = (
            lambda s: f"{s.user.get_full_name() or s.user.username} "
                      f"({s.school_year}. year)"
        )
