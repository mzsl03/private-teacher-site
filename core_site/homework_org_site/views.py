from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from homework_org_site.forms.student_add_form import StudentForm
from homework_org_site.models import Student


@login_required(login_url='/')
def index(request):
    return render(request,"index.html")


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Hibás felhasználónév vagy jelszó!'})
    return render(request, "login.html")

@login_required(login_url='/')
def student_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    students = Student.objects.all()
    return render(request, "student_list.html", {'students': students})

@login_required(login_url='/')
def add_student(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            Student.objects.create(
                user=user,
                school_year = form.cleaned_data['school_year'],
                notes=form.cleaned_data['notes']
            )
            return redirect('home')
    else:
        form = StudentForm()

    return render(request, "add_student.html", {'form': form})
