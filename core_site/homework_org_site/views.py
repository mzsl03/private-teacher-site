import calendar
import json
from collections import defaultdict
from django.utils import timezone
from django.core.cache import cache
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from homework_org_site.forms.homework_add_form import HomeworkForm
from homework_org_site.forms.homework_update_form import HomeworkUpdateForm
from homework_org_site.forms.lesson_add_form import LessonAddForm
from homework_org_site.forms.student_add_form import StudentForm
from homework_org_site.forms.student_update_form import StudentUpdateForm
from homework_org_site.models import Student, Lesson, Homework
from homework_org_site.supportfiles.news_getter import news_getter


@login_required(login_url='/')
def index(request):
    last_update = cache.get("news_last_update")
    news = cache.get("news")
    if not last_update or timezone.now() - last_update > timedelta(days=1):
        news = news_getter()
        cache.set("news_last_update", timezone.now(), 86400)
        cache.set("news", news, 86400)
    news_data = zip(news[0], news[1], news[2])
    return render(request,"index.html", {'news': news_data})


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
    qsh = (Homework.objects
           .filter(due_date__range=(start, end))
           .select_related("student__user", "subject"))

    if hasattr(request.user, "teacher"):
        qs = qs.filter(teacher=request.user.teacher)
    elif hasattr(request.user, "student"):
        qs = qs.filter(student=request.user.student)
        qsh = qsh.filter(student=request.user.student)

    by_day = defaultdict(lambda: {"lessons": [], "homeworks": []})

    for l in qs:
        by_day[l.date]["lessons"].append(l)

    for h in qsh:
        by_day[h.due_date]["homeworks"].append(h)

    weeks = []
    for week in raw_weeks:
        days = []
        for d in week:
            days.append({"date": d,
                         "lessons": by_day[d]["lessons"],
                         "homeworks": by_day[d]["homeworks"]})
        weeks.append(days)

    prev_year, prev_month = (year - 1, 12) if month == 1 else (year, month - 1)
    next_year, next_month = (year + 1, 1)  if month == 12 else (year, month + 1)

    return render(request, "calendar/month.html", {
        "year": year, "month": month, "today": today,
        "weeks": weeks,
        "prev_year": prev_year, "prev_month": prev_month,
        "next_year": next_year, "next_month": next_month,
        "user": request.user,
    })

login_required(login_url='/')
def kanban_board(request, student_id):
    user = request.user
    if hasattr(user, "teacher"):
        student = get_object_or_404(Student, id=student_id)
    else:
        if user.student.id != student_id:
            return redirect('home')
        student = user.student
    todos = Homework.objects.filter(student=student, status="TODO")
    in_progress = Homework.objects.filter(student=student, status="IN_PROGRESS")
    done = Homework.objects.filter(student=student, status="DONE")
    return render(request, 'kanban.html',
                  {
                      'student': student,
                      'todos': todos,
                      'in_progress': in_progress,
                      'done': done,
                  }
                  )

login_required(login_url='/')
def add_homework(request):
    if not request.user.is_superuser:
        return redirect('home')
    form = HomeworkForm()
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            homework = form.save(commit=False)
            if hasattr(request.user, "teacher"):
                homework.teacher = request.user.teacher
            homework.save()
            print(form.cleaned_data.get("student"))
            return redirect("kanban", student_id=homework.student.id)
        form = HomeworkForm()
    return render(request, "add_homework.html", {'form': form})

@csrf_exempt
def update_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        hw_id = data.get("id")
        status = data.get("status")
        try:
            hw = Homework.objects.get(id=hw_id)
            hw.status = status
            hw.save()
            return JsonResponse({"success": True})
        except Homework.DoesNotExist:
            return JsonResponse({"success": False, "error": "Homework not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})

@login_required(login_url='/')
@csrf_exempt
def delete_done_homeworks(request):
    if request.method == "POST":
        deleted_count, _ = Homework.objects.filter(status="DONE").delete()
        return JsonResponse({"success": True, "deleted": deleted_count})
    return JsonResponse({"success": False, "error": "Invalid request"})

@login_required(login_url='/')
def delete_student(request, pk):
    if request.method == "POST":
        student = get_object_or_404(Student, pk=pk)
        user = student.user
        user.delete()
        return redirect("student_list")
    return redirect("student_list")

@login_required(login_url='/')
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    user = student.user

    if request.method == "POST":
        form = StudentUpdateForm(request.POST, user_instance=user)
        if form.is_valid():
            user.username = form.cleaned_data["username"]
            user.email = form.cleaned_data["email"]
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()
            student.school_year = form.cleaned_data["school_year"]
            student.notes = form.cleaned_data["notes"]
            student.save()

            return redirect("student_list")
    else:
        form = StudentUpdateForm(initial={
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "school_year": student.school_year,
            "notes": student.notes,
        }, user_instance=user)

    return render(request, "edit_student.html", {"form": form, "student": student})

@login_required(login_url='/')
def edit_homework(request, pk):
    homework = get_object_or_404(Homework, pk=pk)
    user = request.user
    if request.method == "POST":
        form = HomeworkUpdateForm(request.POST, instance=homework)
        if form.is_valid():
            form.save()
            return redirect("kanban", student_id=homework.student.id)
    else:
        form = HomeworkUpdateForm(instance=homework)

    return render(request, "edit_homework.html", {"form": form, "homework": homework, "user": user})