"""
URL configuration for core_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from homework_org_site import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', views.index, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_lesson/', views.add_lesson, name='add_lesson'),
    path('calendar/', views.calendar_month, name='calendar_month_today'),
    path('calendar/<int:year>/<int:month>/', views.calendar_month, name='calendar_month'),
    path('kanban/<int:student_id>/', views.kanban_board, name='kanban'),
    path('add_homework/', views.add_homework, name='add_homework'),
    path('update_status/', views.update_status, name='update_homework_status'),
    path('delete_done/', views.delete_done_homeworks, name='delete_done_homeworks'),
    path('students/<int:pk>/delete/', views.delete_student, name='delete_student'),
    path('students/<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('homework/<int:pk>/edit/', views.edit_homework, name='edit_homework'),
    path('delete_old_lessons/', views.delete_old_lessons, name='delete_old_lessons'),
    path('lesson/<int:pk>/edit/', views.edit_lesson, name='edit_lesson'),
]
