import cv2
import pickle
import os
import numpy as np
from .models import Student
from django.conf import settings

def train_face_encodings():
    """
    Train face recognition model for all students with face images
    using OpenCV's LBPH Face Recognizer
    """
    try:
        # Get all students with face images
        students = Student.objects.filter(face_image__isnull=False)
        
        if not students:
            return False
        
        # Load face detection model
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Create LBPH face recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Lists to hold face data and corresponding labels
        faces = []
        labels = []
        
        # Create a mapping from label to student_id
        label_to_id = {}
        current_label = 0
        
        # Standardize face size for better recognition
        std_width, std_height = 100, 100
        
        # Process each student's face image
        for student in students:
            if student.face_image and os.path.exists(student.face_image.path):
                # Load and convert the image to grayscale
                img = cv2.imread(student.face_image.path)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                # Detect faces in the image
                detected_faces = face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )
                
                # If a face is detected, add it to training data with augmentations
                if len(detected_faces) > 0:
                    for (x, y, w, h) in detected_faces:
                        face_roi = gray[y:y+h, x:x+w]
                        
                        # Resize all face ROIs to a standard size
                        face_roi = cv2.resize(face_roi, (std_width, std_height))
                        
                        # Add original face
                        faces.append(face_roi)
                        labels.append(current_label)
                        
                        # Add slightly rotated versions for better angle coverage
                        rows, cols = face_roi.shape
                        for angle in [-10, -5, 5, 10]:
                            M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
                            rotated = cv2.warpAffine(face_roi, M, (cols, rows))
                            faces.append(rotated)
                            labels.append(current_label)
                        
                        # Add slightly brightness-adjusted versions
                        for alpha in [0.8, 1.2]:  # Darken and brighten
                            adjusted = cv2.convertScaleAbs(face_roi, alpha=alpha, beta=0)
                            faces.append(adjusted)
                            labels.append(current_label)
                    
                    # Map this label to student id
                    label_to_id[current_label] = student.id
                    
                    # Increment label for next student
                    current_label += 1
                    
                    # Mark student as encoded
                    student.face_encoded = True
                    student.save()
        
        # Save the label mapping
        label_mapping_path = os.path.join(settings.FACE_ENCODINGS_DIR, 'label_mapping.pkl')
        with open(label_mapping_path, 'wb') as f:
            pickle.dump(label_to_id, f)
        
        # Train the model if we have data
        if faces and labels:
            recognizer.train(faces, np.array(labels))
            
            # Save the trained model
            model_path = os.path.join(settings.FACE_ENCODINGS_DIR, 'opencv_model.yml')
            recognizer.write(model_path)
            
            # Also save a compatibility file for the recognizer.py
            encodings_data = {}
            for label, student_id in label_to_id.items():
                encodings_data[student_id] = True  # Just a placeholder to check existence
            
            # Save encodings file for compatibility
            encodings_path = os.path.join(settings.FACE_ENCODINGS_DIR, 'encodings.pkl')
            with open(encodings_path, 'wb') as f:
                pickle.dump(encodings_data, f)
            
            return True
        else:
            print("No face data available for training")
            return False
        
    except Exception as e:
        print(f"Error in training face encodings: {e}")
        return False
