from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from homework_org_site.models import Student

class StudentUpdateForm(forms.ModelForm):

    username = forms.CharField(max_length=150, label='Username')
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(max_length=255, label="First Name")
    last_name = forms.CharField(max_length=255, label="Last Name")
    school_year = forms.IntegerField(min_value=1, max_value=12, label="School year")
    notes = forms.CharField(max_length=200, label="Notes on student", required=False)

    class Meta:
        model = Student
        fields = ["school_year", "notes"]

    def __init__(self, *args, user_instance=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_instance = user_instance

    def clean_username(self):
        username = self.cleaned_data.get("username")
        existing_user = User.objects.filter(username=username).exclude(pk=self.user_instance.pk)
        if existing_user.exists():
            raise ValidationError("Username already exists!")
        return username