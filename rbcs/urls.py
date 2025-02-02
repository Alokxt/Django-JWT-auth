from django.contrib import admin
from django.urls import path
from rbcs import views


urlpatterns = [
    path('auth/login/',views.login_view , name='login'),
    path('school/dashboard/', views.school_dashboard, name='school_dashboard'),
    path('parent/dashboard/',views.parent_dash,name="parents_dash"),
    path('student/dashboard/',views.student_dash,name="students_dash"),
    path('student/achievements/<int:student_id>/',views.student_acheivemnets,name="student_acheivements"),
    path('request-password-reset/', views.reset_password, name='password-reset'),
    path('reset-password/<uidb64>/<token>/', views.fortgot, name='forgot-password'),
    path('',views.get_to_login,name="login_page")
]
