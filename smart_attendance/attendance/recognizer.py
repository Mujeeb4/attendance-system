import cv2
import pickle
import os
import numpy as np
from django.conf import settings

def recognize_faces_in_image(image_path, student_ids=None):
    """
    Recognize faces in the given image using OpenCV and face recognition
    
    Args:
        image_path: Path to the image file
        student_ids: List of student IDs to limit recognition to (optional)
        
    Returns:
        List of student IDs that were recognized in the image
    """
    try:
        # Check if the encodings file exists
        encodings_path = os.path.join(settings.FACE_ENCODINGS_DIR, 'encodings.pkl')
        if not os.path.exists(encodings_path):
            print("No encodings file found.")
            return []
        
        # Load the encodings
        with open(encodings_path, 'rb') as f:
            known_encodings_data = pickle.load(f)
        
        # If student_ids is provided, filter the encodings to only include those students
        if student_ids:
            known_encodings_data = {k: v for k, v in known_encodings_data.items() if k in student_ids}
        
        if not known_encodings_data:
            print("No encodings data available for the specified students.")
            return []
        
        # Load multiple face detection models
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        if not os.path.exists(cascade_path):
            print(f"Error: Face cascade file not found at {cascade_path}")
            return []
            
        face_cascade = cv2.CascadeClassifier(cascade_path)
        if face_cascade.empty():
            print("Error: Could not load face cascade classifier")
            return []
        
        profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
        
        # Load the LBPH face recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # If we've already trained the model, load it
        model_path = os.path.join(settings.FACE_ENCODINGS_DIR, 'opencv_model.yml')
        if os.path.exists(model_path):
            try:
                recognizer.read(model_path)
            except Exception as e:
                print(f"Error loading model file: {e}")
                return []
        else:
            print("No OpenCV model found. Please train the model first.")
            return []
            
        # Load the image
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Enhance the image before face detection
        gray = cv2.equalizeHist(gray)  # Improve contrast
        
        # Detect faces with frontal cascade
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Also try to detect profile faces
        profile_faces = profile_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Combine detections (may need to handle overlaps)
        all_faces = list(faces) + list(profile_faces)
        
        # List to store recognized student IDs
        recognized_student_ids = []
        
        # Map labels to student IDs - should be loaded from a mapping file created during training
        label_to_id_path = os.path.join(settings.FACE_ENCODINGS_DIR, 'label_mapping.pkl')
        if os.path.exists(label_to_id_path):
            with open(label_to_id_path, 'rb') as f:
                label_to_id = pickle.load(f)
        else:
            print("No label mapping found. Please train the model first.")
            return []
            
        # Create a mapping of student_id to confidence score
        student_confidence = {}

        # For each detected face
        for (x, y, w, h) in faces:
            # Recognize the face
            face_roi = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(face_roi)
            
            # If confidence is low enough (lower is better in OpenCV's LBPH)
            if confidence < 100:  # Threshold can be adjusted
                student_id = label_to_id.get(label)
                if student_id:
                    # Keep track of the best confidence score for each student
                    if student_id not in student_confidence or confidence < student_confidence[student_id]:
                        student_confidence[student_id] = confidence

        # Add students with the best confidence scores
        recognized_student_ids = list(student_confidence.keys())
                    
        return recognized_student_ids
        
    except Exception as e:
        print(f"Error in face recognition: {e}")
        return []
