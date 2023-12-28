import cv2
from tkinter import messagebox
from db.database import Database

class DatasetGenerator:
    def __init__(self, gui_instance):
        self.db = Database()
        self.gui = gui_instance

    def generate_dataset(self):
        try:
            if self.gui.t1.get() == "" or self.gui.t2.get() == "" or self.gui.t3.get() == "":
                messagebox.showinfo('Result', 'Please provide complete details of the user')
                return

            myresult = self.db.collection.find()
            user_id = self.db.collection.count_documents({}) + 1

            user_data = {"_id": user_id, "Name": self.gui.t1.get(), "Age": self.gui.t2.get(), "Address": self.gui.t3.get()}
            self.db.collection.insert_one(user_data)

            face_classifier = cv2.CascadeClassifier("./haarcascade/haarcascade_frontalface_default.xml")

            def face_cropped(img):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5)

                if faces == ():
                    return None
                for (x, y, w, h) in faces:
                    cropped_face = img[y:y+h, x:x+w]
                return cropped_face

            cap = cv2.VideoCapture(0)
            img_id = 0

            while True:
                ret, frame = cap.read()
                if face_cropped(frame) is not None:
                    img_id += 1
                    face = cv2.resize(face_cropped(frame), (200, 200))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    file_name_path = f"data/user.{user_id}.{img_id}.jpg"
                    cv2.imwrite(file_name_path, face)
                    cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

                    cv2.imshow("Cropped face", face)
                    if cv2.waitKey(1) == 13 or int(img_id) == 200:
                        break

            cap.release()
            cv2.destroyAllWindows()
            print('Generating dataset completed!!!')

        except Exception as e:
            print(f'Error in dataset generation: {str(e)}')

if __name__ == "__main__":
    from gui import FaceRecognitionGUI
    gui_instance = FaceRecognitionGUI(None)
    generator = DatasetGenerator(gui_instance)
    generator.generate_dataset()
