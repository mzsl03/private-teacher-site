from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

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
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('home')
    students = Student.objects.all()
    return render(request, "student_list.html", {'students': students})