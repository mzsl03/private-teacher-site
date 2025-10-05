import calendar
from collections import defaultdict
from datetime import date
from django.utils import timezone
from django.shortcuts import render

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from homework_org_site.forms.lesson_add_form import LessonAddForm
from homework_org_site.forms.student_add_form import StudentForm
from homework_org_site.models import Student, Lesson


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

@login_required(login_url='/')
def add_lesson(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == "POST":
        form = LessonAddForm(request.POST, user=request.user)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.teacher = request.user.teacher
            lesson.save()
            return redirect("calendar_month_today")
    else:
        form = LessonAddForm(user=request.user)
    return render(request, "add_lesson.html", {"form": form})

login_required(login_url='/')
def calendar_month(request, year=None, month=None):
    today = timezone.localdate()
    if year is None or month is None:
        year, month = today.year, today.month

    cal = calendar.Calendar(firstweekday=0)
    raw_weeks = cal.monthdatescalendar(year, month)

    start = raw_weeks[0][0]
    end = raw_weeks[-1][-1]
    qs = (Lesson.objects
          .filter(date__range=(start, end))
          .select_related("student__user", "teacher__user", "subject"))

    if hasattr(request.user, "teacher"):
        qs = qs.filter(teacher=request.user.teacher)
    elif hasattr(request.user, "student"):
        qs = qs.filter(student=request.user.student)

    by_day = defaultdict(list)
    for l in qs:
        by_day[l.date].append(l)

    weeks = []
    for week in raw_weeks:
        days = []
        for d in week:
            days.append({"date": d, "lessons": by_day.get(d, [])})
        weeks.append(days)

    prev_year, prev_month = (year - 1, 12) if month == 1 else (year, month - 1)
    next_year, next_month = (year + 1, 1)  if month == 12 else (year, month + 1)

    return render(request, "calendar/month.html", {
        "year": year, "month": month, "today": today,
        "weeks": weeks,
        "prev_year": prev_year, "prev_month": prev_month,
        "next_year": next_year, "next_month": next_month,
    })