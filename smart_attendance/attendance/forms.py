from django import forms
from .models import Student, ClassGroup, AttendanceRecord, AttendanceDetail
import os

class StudentFaceUploadForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['face_image']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'student_id', 'face_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'face_image': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control'})
        }

class ClassPhotoUploadForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control'})
        }
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file extension
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError("Only JPG and PNG files are allowed.")
            
            # Check file size (max 10MB)
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Image file is too large (>10MB).")
                
        return image

class AttendanceConfirmationForm(forms.Form):
    student_ids = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, students, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_ids'].choices = [(s.id, s.name) for s in students]

class AttendanceEditForm(forms.ModelForm):
    class Meta:
        model = AttendanceDetail
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})
        }
