from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    face_image = models.ImageField(upload_to='student_faces/', null=True, blank=True)
    face_encoded = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} ({self.student_id})"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.user.get_full_name() or self.user.username

class ClassGroup(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classes')
    students = models.ManyToManyField(Student, related_name='classes')
    
    def __str__(self):
        return f"{self.name} - {self.teacher}"
    
    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"

class AttendanceRecord(models.Model):
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)
    date = models.DateField()
    recorded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='attendance_images/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['class_group', 'date']
        
    def __str__(self):
        return f"{self.class_group} on {self.date}"

class AttendanceDetail(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('excused', 'Excused'),
        ('late', 'Late'),
    )
    
    record = models.ForeignKey(AttendanceRecord, on_delete=models.CASCADE, related_name='details')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')
    marked_by_ai = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['record', 'student']
    
    def __str__(self):
        return f"{self.student.name} - {self.status} on {self.record.date}"

class AttendanceChangeLog(models.Model):
    detail = models.ForeignKey(AttendanceDetail, on_delete=models.CASCADE)
    previous_status = models.CharField(max_length=10, choices=AttendanceDetail.STATUS_CHOICES)
    new_status = models.CharField(max_length=10, choices=AttendanceDetail.STATUS_CHOICES)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
