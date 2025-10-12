from django import forms

from homework_org_site.models import Lesson

class LessonUpdateForm(forms.ModelForm):

    class Meta:
        model = Lesson
        fields = ['date', 'duration', 'topic']
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            'duration': forms.NumberInput(attrs={'min': 15, 'step': 15}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].label = "Date"
        self.fields["duration"].label = "Duration"
        self.fields["topic"].label = "Topic"