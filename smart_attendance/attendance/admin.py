from django.contrib import admin
from .models import Student, Teacher, ClassGroup, AttendanceRecord, AttendanceDetail, AttendanceChangeLog

class AttendanceDetailInline(admin.TabularInline):
    model = AttendanceDetail
    extra = 0

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'student_id', 'face_encoded']
    search_fields = ['name', 'student_id']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'teacher_id']

@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher']
    filter_horizontal = ['students']

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['class_group', 'date', 'recorded_by', 'timestamp']
    list_filter = ['date', 'class_group', 'recorded_by']
    inlines = [AttendanceDetailInline]

@admin.register(AttendanceDetail)
class AttendanceDetailAdmin(admin.ModelAdmin):
    list_display = ['student', 'record', 'status', 'marked_by_ai']
    list_filter = ['status', 'marked_by_ai', 'record__date']

@admin.register(AttendanceChangeLog)
class AttendanceChangeLogAdmin(admin.ModelAdmin):
    list_display = ['detail', 'previous_status', 'new_status', 'changed_by', 'timestamp']
    list_filter = ['timestamp', 'previous_status', 'new_status']
    readonly_fields = ['detail', 'previous_status', 'new_status', 'changed_by', 'timestamp']
