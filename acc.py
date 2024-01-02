# gui.py
import os
import cv2
import numpy as np
from PIL import Image
from tkinter import messagebox
import tkinter as tk
# from tkinter import ttk
from PIL import ImageTk
from view.about_tab import AboutTab 
from tkinter import ttk, filedialog, messagebox

# Load the trained LBPH Face Recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('./classifier/classifier.xml')

# Load the image you want to predict
new_image = cv2.imread('C:/Users/Aman Yadav/Desktop/video/win.jpg', cv2.IMREAD_GRAYSCALE)


# Perform face detection on the new image
face_cascade = cv2.CascadeClassifier('./haarcascade/haarcascade_frontalface_default.xml')
faces = face_cascade.detectMultiScale(new_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Iterate over detected faces and make predictions
for (x, y, w, h) in faces:
    face_roi = new_image[y:y + h, x:x + w]
    
    # Perform prediction
    label, confidence = recognizer.predict(face_roi)
    
    # Print the predicted label and confidence
    print(f'Predicted Label: {label}, Confidence: {confidence}')

    # Draw a rectangle around the detected face
    color = (255, 0, 0)  # BGR format
    thickness = 2
    cv2.rectangle(new_image, (x, y), (x + w, y + h), color, thickness)

# Display the new image with rectangles around detected faces
cv2.imshow('Predictions', new_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
