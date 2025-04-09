from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('class/<int:class_id>/', views.class_detail, name='class_detail'),
    path('class/<int:class_id>/upload/', views.upload_attendance, name='upload_attendance'),
    path('class/<int:class_id>/confirm/', views.confirm_attendance, name='confirm_attendance'),
    path('class/<int:class_id>/calendar/', views.attendance_calendar, name='calendar'),
    path('class/<int:class_id>/calendar/<str:date>/', views.edit_attendance, name='edit_attendance'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:student_id>/upload-face/', views.upload_student_face, name='upload_student_face'),
    path('train-model/', views.train_model_view, name='train_model'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
]
