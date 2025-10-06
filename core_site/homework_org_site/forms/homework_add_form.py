from email.policy import default

from django import forms
from homework_org_site.models import Homework, Lesson, Subject, Student

class HomeworkForm(forms.ModelForm):
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
        model = Homework
        fields = ["title", "description", "due_date", "subject", "student", "status"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def save(self, commit=True):
        homework = super().save(commit=False)
        if not homework.status:
            homework.status = "TODO"
        if commit:
            homework.save()
        return homework

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
