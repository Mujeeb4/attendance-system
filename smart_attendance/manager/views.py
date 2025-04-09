from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib import messages
from attendance.models import Student, Teacher, ClassGroup
from .forms import TeacherForm, StudentForm, ClassGroupForm, UserForm
from django.db import transaction

def is_manager(user):
    """Check if user is a manager"""
    return user.is_staff and user.is_authenticated

@login_required
@user_passes_test(is_manager)
def dashboard(request):
    """Manager dashboard showing overview of system data"""
    total_teachers = Teacher.objects.count()
    total_students = Student.objects.count()
    total_classes = ClassGroup.objects.count()
    
    recent_teachers = Teacher.objects.all().order_by('-id')[:5]
    recent_students = Student.objects.all().order_by('-id')[:5]
    recent_classes = ClassGroup.objects.all().order_by('-id')[:5]
    
    context = {
        'total_teachers': total_teachers,
        'total_students': total_students,
        'total_classes': total_classes,
        'recent_teachers': recent_teachers,
        'recent_students': recent_students,
        'recent_classes': recent_classes,
    }
    
    return render(request, 'manager/dashboard.html', context)

# Teacher Management
@login_required
@user_passes_test(is_manager)
def teacher_list(request):
    """List all teachers"""
    teachers = Teacher.objects.all()
    return render(request, 'manager/teacher_list.html', {'teachers': teachers})

@login_required
@user_passes_test(is_manager)
def add_teacher(request):
    """Add a new teacher"""
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        teacher_form = TeacherForm(request.POST)
        
        if user_form.is_valid() and teacher_form.is_valid():
            with transaction.atomic():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()
                
                teacher = teacher_form.save(commit=False)
                teacher.user = user
                teacher.save()
                
                messages.success(request, f"Teacher {teacher.user.get_full_name() or teacher.user.username} has been added")
                return redirect('manager:teacher_list')
    else:
        user_form = UserForm()
        teacher_form = TeacherForm()
    
    return render(request, 'manager/add_teacher.html', {
        'user_form': user_form,
        'teacher_form': teacher_form
    })

@login_required
@user_passes_test(is_manager)
def edit_teacher(request, teacher_id):
    """Edit an existing teacher"""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=teacher.user)
        teacher_form = TeacherForm(request.POST, instance=teacher)
        
        if user_form.is_valid() and teacher_form.is_valid():
            with transaction.atomic():
                user = user_form.save()
                teacher = teacher_form.save()
                
                messages.success(request, f"Teacher {teacher.user.get_full_name() or teacher.user.username} has been updated")
                return redirect('manager:teacher_list')
    else:
        user_form = UserForm(instance=teacher.user)
        teacher_form = TeacherForm(instance=teacher)
    
    return render(request, 'manager/edit_teacher.html', {
        'user_form': user_form,
        'teacher_form': teacher_form,
        'teacher': teacher
    })

# Student Management
@login_required
@user_passes_test(is_manager)
def student_list(request):
    """List all students"""
    students = Student.objects.all()
    return render(request, 'manager/student_list.html', {'students': students})

@login_required
@user_passes_test(is_manager)
def add_student(request):
    """Add a new student"""
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"Student {student.name} has been added")
            return redirect('manager:student_list')
    else:
        form = StudentForm()
    
    return render(request, 'manager/add_student.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def edit_student(request, student_id):
    """Edit an existing student"""
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"Student {student.name} has been updated")
            return redirect('manager:student_list')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'manager/edit_student.html', {'form': form, 'student': student})

# Class Management
@login_required
@user_passes_test(is_manager)
def class_list(request):
    """List all classes"""
    classes = ClassGroup.objects.all()
    return render(request, 'manager/class_list.html', {'classes': classes})

@login_required
@user_passes_test(is_manager)
def add_class(request):
    """Add a new class"""
    if request.method == 'POST':
        form = ClassGroupForm(request.POST)
        if form.is_valid():
            class_group = form.save()
            messages.success(request, f"Class {class_group.name} has been added")
            return redirect('manager:class_list')
    else:
        form = ClassGroupForm()
    
    return render(request, 'manager/add_class.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def edit_class(request, class_id):
    """Edit an existing class"""
    class_group = get_object_or_404(ClassGroup, id=class_id)
    
    if request.method == 'POST':
        form = ClassGroupForm(request.POST, instance=class_group)
        if form.is_valid():
            class_group = form.save()
            messages.success(request, f"Class {class_group.name} has been updated")
            return redirect('manager:class_list')
    else:
        form = ClassGroupForm(instance=class_group)
    
    return render(request, 'manager/edit_class.html', {'form': form, 'class_group': class_group})
