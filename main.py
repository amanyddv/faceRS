# main.py
from face_recognition_system import FaceRecognitionSystem

if __name__ == "__main__":
    face_recognition_system = FaceRecognitionSystem()
    screen_width = face_recognition_system.window.winfo_screenwidth()
    screen_height = face_recognition_system.window.winfo_screenheight()
    face_recognition_system.window.geometry(f"{screen_width}x{screen_height}")
    face_recognition_system.window.mainloop()
