from django import forms

from homework_org_site.models import Homework

class HomeworkUpdateForm(forms.ModelForm):

    class Meta:
        model = Homework
        fields = ['title', 'description', 'due_date']
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].label = "Title"
        self.fields["description"].label = "Description"
        self.fields["due_date"].label = "Due date"