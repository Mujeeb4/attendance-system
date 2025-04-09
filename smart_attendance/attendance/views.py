from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponseForbidden, Http404
from .models import Student, Teacher, ClassGroup, AttendanceRecord, AttendanceDetail, AttendanceChangeLog
from .forms import StudentFaceUploadForm, ClassPhotoUploadForm, AttendanceConfirmationForm, AttendanceEditForm
from manager.forms import StudentForm
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import datetime
from .train_model import train_face_encodings
from .recognizer import recognize_faces_in_image
import os
import json
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

def is_manager(user):
    return user.is_staff

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect based on user role
            if user.is_staff:
                return redirect('manager:dashboard')
            try:
                # Check if user is a teacher
                teacher = Teacher.objects.get(user=user)
                return redirect('attendance:dashboard')
            except Teacher.DoesNotExist:
                try:
                    # Check if user is a student
                    student = Student.objects.get(user=user)
                    return redirect('attendance:student_dashboard')
                except Student.DoesNotExist:
                    messages.error(request, "Account exists but not assigned to any role")
                    logout(request)
        else:
            messages.error(request, "Invalid credentials")
    
    return render(request, 'attendance/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('attendance:login')

@login_required
def dashboard(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        classes = teacher.classes.all()
        return render(request, 'attendance/dashboard.html', {'classes': classes})
    except Teacher.DoesNotExist:
        messages.error(request, "You are not registered as a teacher")
        return redirect('attendance:logout')

@login_required
def class_detail(request, class_id):
    class_group = get_object_or_404(ClassGroup, id=class_id)
    
    # Check if the logged-in user is the teacher of this class
    if class_group.teacher.user != request.user:
        return HttpResponseForbidden("You don't have permission to view this class")
    
    students = class_group.students.all()
    return render(request, 'attendance/class_detail.html', {'class': class_group, 'students': students})

@login_required
def upload_attendance(request, class_id):
    class_group = get_object_or_404(ClassGroup, id=class_id)
    
    # Check if the logged-in user is the teacher of this class
    if class_group.teacher.user != request.user:
        return HttpResponseForbidden("You don't have permission to mark attendance for this class")
    
    if request.method == 'POST':
        form = ClassPhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if attendance record already exists for today
            today = timezone.now().date()
            attendance_record, created = AttendanceRecord.objects.get_or_create(
                class_group=class_group,
                date=today,
                defaults={
                    'recorded_by': class_group.teacher,
                    'image': form.cleaned_data['image']
                }
            )
            
            if not created:
                attendance_record.image = form.cleaned_data['image']
                attendance_record.save()
            
            # Process the image with face recognition
            recognized_students, faces_detected = recognize_faces_in_image(
                attendance_record.image.path, 
                student_ids=[s.id for s in class_group.students.all()]
            )
            
            # Add warning if no faces are detected
            if not recognized_students and faces_detected == 0:
                messages.warning(request, "No faces were detected in the uploaded image. Please try a clearer photo.")
                return redirect('attendance:upload_attendance', class_id=class_id)
            
            # Save temporary recognition results for confirmation
            request.session['recognized_students'] = recognized_students
            request.session['attendance_record_id'] = attendance_record.id
            
            return redirect('attendance:confirm_attendance', class_id=class_id)
    else:
        form = ClassPhotoUploadForm()
    
    return render(request, 'attendance/upload.html', {'form': form, 'class': class_group})

@login_required
def confirm_attendance(request, class_id):
    class_group = get_object_or_404(ClassGroup, id=class_id)
    
    # Check if the logged-in user is the teacher of this class
    if class_group.teacher.user != request.user:
        return HttpResponseForbidden("You don't have permission to confirm attendance for this class")
    
    # Get the recognized students from session
    recognized_student_ids = request.session.get('recognized_students', [])
    attendance_record_id = request.session.get('attendance_record_id')
    
    if not recognized_student_ids or not attendance_record_id:
        messages.error(request, "No recognition data available. Please upload a photo first.")
        return redirect('attendance:upload_attendance', class_id=class_id)
    
    attendance_record = get_object_or_404(AttendanceRecord, id=attendance_record_id)
    all_students = class_group.students.all()
    recognized_students = Student.objects.filter(id__in=recognized_student_ids)
    
    if request.method == 'POST':
        # Get the students confirmed as present by the teacher
        confirmed_student_ids = request.POST.getlist('student_ids')
        confirmed_students = Student.objects.filter(id__in=confirmed_student_ids)
        
        # Mark all students as absent initially
        for student in all_students:
            AttendanceDetail.objects.update_or_create(
                record=attendance_record,
                student=student,
                defaults={
                    'status': 'absent',
                    'marked_by_ai': student.id in recognized_student_ids
                }
            )
        
        # Then update the confirmed students as present
        for student in confirmed_students:
            AttendanceDetail.objects.update_or_create(
                record=attendance_record,
                student=student,
                defaults={
                    'status': 'present',
                    'marked_by_ai': student.id in recognized_student_ids
                }
            )
        
        # Clear session data
        if 'recognized_students' in request.session:
            del request.session['recognized_students']
        if 'attendance_record_id' in request.session:
            del request.session['attendance_record_id']
        
        messages.success(request, f"Attendance for {class_group.name} has been recorded successfully.")
        return redirect('attendance:class_detail', class_id=class_id)
    
    initial_selected = [student.id for student in recognized_students]
    form = AttendanceConfirmationForm(
        students=all_students, 
        initial={'student_ids': initial_selected}
    )
    
    return render(request, 'attendance/confirm_attendance.html', {
        'form': form, 
        'class': class_group,
        'recognized_students': recognized_students,
        'all_students': all_students
    })

@login_required
def attendance_calendar(request, class_id):
    class_group = get_object_or_404(ClassGroup, id=class_id)
    
    # Check if the logged-in user is the teacher of this class
    if class_group.teacher.user != request.user:
        return HttpResponseForbidden("You don't have permission to view attendance for this class")
    
    # Get attendance records for this class
    attendance_records = AttendanceRecord.objects.filter(class_group=class_group).order_by('-date')
    
    # Create a dictionary of dates with attendance data
    calendar_data = {}
    for record in attendance_records:
        present_count = record.details.filter(status='present').count()
        total_count = record.details.count()
        calendar_data[str(record.date)] = {
            'record_id': record.id,
            'present_count': present_count,
            'total_count': total_count,
        }
    
    return render(request, 'attendance/calendar.html', {
        'class': class_group,
        'calendar_data': json.dumps(calendar_data)
    })

@login_required
def edit_attendance(request, class_id, date):
    class_group = get_object_or_404(ClassGroup, id=class_id)
    
    # Check if the logged-in user is the teacher of this class
    if class_group.teacher.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit attendance for this class")
    
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        raise Http404("Invalid date format")
    
    # Get or create attendance record for this date
    attendance_record, created = AttendanceRecord.objects.get_or_create(
        class_group=class_group,
        date=date_obj,
        defaults={'recorded_by': class_group.teacher}
    )
    
    # Ensure all students have an attendance detail
    students = class_group.students.all()
    for student in students:
        AttendanceDetail.objects.get_or_create(
            record=attendance_record,
            student=student,
            defaults={'status': 'absent'}
        )
    
    # Get all attendance details for this record
    attendance_details = AttendanceDetail.objects.filter(record=attendance_record)
    
    if request.method == 'POST':
        # Update attendance status for each student
        for detail in attendance_details:
            new_status = request.POST.get(f'status_{detail.student.id}')
            if new_status and new_status != detail.status:
                # Log the change
                AttendanceChangeLog.objects.create(
                    detail=detail,
                    previous_status=detail.status,
                    new_status=new_status,
                    changed_by=request.user
                )
                
                # Update the status
                detail.status = new_status
                detail.save()
        
        messages.success(request, f"Attendance for {date} has been updated successfully.")
        return redirect('attendance:calendar', class_id=class_id)
    
    # Prepare forms for each student
    student_forms = []
    for detail in attendance_details:
        form = AttendanceEditForm(instance=detail, prefix=f'student_{detail.student.id}')
        student_forms.append({
            'student': detail.student,
            'form': form,
            'detail': detail
        })
    
    return render(request, 'attendance/edit_attendance.html', {
        'class': class_group,
        'date': date,
        'student_forms': student_forms
    })

@login_required
def add_student(request):
    # Check if the user is admin or has permission
    if not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to add students")
    
    if request.method == 'POST':
        # Process student creation form
        pass
    
    return render(request, 'attendance/add_student.html')

@login_required
def upload_student_face(request, student_id):
    # Check if the user is admin or has permission
    if not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to upload student faces")
    
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = StudentFaceUploadForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f"Face image for {student.name} uploaded successfully.")
            return redirect('attendance:train_model')
    else:
        form = StudentFaceUploadForm(instance=student)
    
    return render(request, 'attendance/upload_student_face.html', {'form': form, 'student': student})

@login_required
def train_model_view(request):
    # Check if the user is admin or has permission
    if not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to train the model")
    
    if request.method == 'POST':
        result = train_face_encodings()
        if result:
            messages.success(request, "Face recognition model trained successfully.")
        else:
            messages.error(request, "Error training face recognition model.")
    
    students_with_faces = Student.objects.filter(face_image__isnull=False)
    students_without_faces = Student.objects.filter(face_image__isnull=True)
    
    return render(request, 'attendance/train_model.html', {
        'students_with_faces': students_with_faces,
        'students_without_faces': students_without_faces
    })

@login_required
def student_dashboard(request):
    """Dashboard for students to view their attendance"""
    try:
        student = Student.objects.get(user=request.user)
        # Get all attendance records for classes this student is in
        attendance_details = AttendanceDetail.objects.filter(
            student=student
        ).select_related('record', 'record__class_group').order_by('-record__date')
        
        # Group by class
        classes = {}
        for detail in attendance_details:
            class_group = detail.record.class_group
            if class_group.id not in classes:
                classes[class_group.id] = {
                    'name': class_group.name,
                    'teacher': class_group.teacher.user.get_full_name() or class_group.teacher.user.username,
                    'records': []
                }
            classes[class_group.id]['records'].append({
                'date': detail.record.date,
                'status': detail.status,
                'marked_by_ai': detail.marked_by_ai
            })
        
        return render(request, 'attendance/student_dashboard.html', {
            'student': student,
            'classes': classes.values()
        })
    except Student.DoesNotExist:
        messages.error(request, "You are not registered as a student")
        return redirect('attendance:logout')

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
