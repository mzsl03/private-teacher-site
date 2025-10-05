from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from homework_org_site.models import Student


class StudentForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label='Username',
        error_messages={
            "invalid": "Invalid username! (Must consist of letters, numbers and the characters '@/./+/-/_ ' only.)"},
    )
    email = forms.EmailField(
        label='Email',
        error_messages={"invalid": "Invalid email!"}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        label='Password'
    )
    first_name = forms.CharField(
        max_length=255,
        label="First Name"
    )
    last_name = forms.CharField(
        max_length=255,
        label="Last Name"
    )
    address = forms.CharField(
        max_length=255,
        label="Address"
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date of Birth"
    )
    phone_number = forms.CharField(
        max_length=12,
        label="Phone number",
        error_messages={"invalid": "Invalid phone number!"}
    )
    school_year = forms.IntegerField(
        min_value=1,
        max_value=12,
        label="School year",
        error_messages={"invalid": "Invalid school year! (Must be between 1 and 12)"}
    )
    notes = forms.CharField(
        max_length=200,
        label="Notes on student"
    )


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists!")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError("Passwords do not match!")
        return cleaned_data