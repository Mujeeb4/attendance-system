# Smart Attendance System

## Overview
Smart Attendance System is a Django-based web application that leverages facial recognition technology to automate student attendance tracking in educational institutions. The system allows teachers to take attendance by simply uploading a classroom photo, which is then processed to identify students using facial recognition algorithms.

## Key Features

### For Teachers
- **Dashboard**: View assigned classes and attendance statistics
- **Class Management**: Access detailed class information and student lists
- **Automated Attendance**: Take attendance by uploading class photos
- **Manual Verification**: Review and adjust AI-detected attendance records
- **Attendance Calendar**: View attendance records by date with color-coded indicators
- **Attendance Editing**: Modify past attendance records with change tracking

### For Students
- **Dashboard**: View personal attendance records across all classes
- **Attendance Status**: Check detailed attendance status (present, absent, late, excused)
- **Attendance Statistics**: View personal attendance rate visualizations

### For Managers/Administrators
- **Comprehensive Dashboard**: Overview of entire system with statistics
- **Teacher Management**: Add, edit, and manage teacher accounts
- **Student Management**: Register students and manage their information
- **Class Management**: Create and configure classes, assign teachers and students
- **Face Recognition Training**: Train the system with student face images

## Technology Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (default), compatible with PostgreSQL
- **Face Recognition**: OpenCV and face_recognition libraries
- **Charts and Visualization**: Chart.js
- **Calendar Interface**: FullCalendar

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Pip (Python package manager)
- Git (optional)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/attendance-system.git
cd attendance-system
```

### Step 2: Create and Activate a Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up the Database
```bash
cd smart_attendance
python manage.py migrate
```

### Step 5: Create a Superuser
```bash
python manage.py createsuperuser
```

### Step 6: Run the Development Server
```bash
python manage.py runserver
```

The application should now be accessible at: http://127.0.0.1:8000/

## Project Structure
attendance-system/
├── smart_attendance/         # Main Django project directory
│   ├── smart_attendance/     # Project settings
│   ├── attendance/           # Attendance app (main functionality)
│   │   ├── models.py         # Database models
│   │   ├── views.py          # View functions
│   │   ├── forms.py          # Form definitions
│   │   ├── urls.py           # URL routing
│   │   ├── recognizer.py     # Face recognition logic
│   │   ├── train_model.py    # Model training functionality
│   │   ├── templates/        # HTML templates
│   │   └── static/           # Static files (CSS, JS)
│   │
│   ├── manager/              # Manager app (administrative functions)
│   │   ├── models.py         # Database models
│   │   ├── views.py          # View functions
│   │   ├── forms.py          # Form definitions
│   │   ├── urls.py           # URL routing
│   │   ├── templates/        # HTML templates
│   │   └── static/           # Static files (CSS, JS)
│   │
│   └── media/                # User-uploaded files (images)
├── requirements.txt          # Python dependencies
└── README.md                 # This file

### Usage Guide
# Manager/Administrator
1- Log in with your admin account
2- First, add teachers through the Teacher Management section
3- Add students with their details and face images
4- Create classes and assign teachers and students to them
5- Train the face recognition model using the collected face images
# Teachers
1- Log in with your teacher account
2- Select a class from your dashboard
3- To take attendance, click "Take Attendance" and upload a photo 4- of the class
5- Review the automatically detected students and make any necessary adjustments
6- Save the attendance record
7- View the attendance calendar to see past records and edit them if needed
# Students
1- Log in with your student account
2- View your attendance status across all enrolled classes
3- Check your attendance statistics
### Security Considerations
1- Student face images are stored securely and used only for attendance purposes
2- Access controls ensure data is only accessible to authorized users
3- Attendance change logs track all modifications to attendance records
### License
This project is licensed under the MIT License - see the LICENSE file for details.

### Support and Contribution
For support, feature requests, or contributions, please open an issue on the GitHub repository or contact the project maintainers.