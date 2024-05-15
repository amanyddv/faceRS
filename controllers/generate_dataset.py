import cv2
import os
from tkinter import messagebox
from db.database import Database
import re


class DatasetGenerator:
    def __init__(self, gui_instance):
        self.db = Database()
        self.gui = gui_instance

    def validate_fields(self):
        # Check for empty fields
        mandatory_fields = {
            "Name": self.gui.name.get(),
            "VID": self.gui.vid.get(),
            "Address": self.gui.address.get(),
            "Phone": self.gui.phone.get(),
            "DOB": self.gui.dob.get(),
            "Father's Name": self.gui.fatherName.get(),
            "Pin Code": self.gui.pinCode.get(),
            "State": self.gui.state.get(),
            "City": self.gui.city.get(),
        }

        for field_name, field_value in mandatory_fields.items():
            if field_value.strip() == "":
                messagebox.showinfo("Result", f"{field_name} cannot be empty")
                return False
            
        vid = (self.gui.vid.get())

        if not vid.isdigit():
            messagebox.showinfo("Result", "VID must contain only digits")
            return False

        if len(vid) <= 5:
            messagebox.showinfo("Result", "VID must be longer than 5 digits")
            return False

        if not re.match(r"^\d{10}$", self.gui.phone.get()):
            messagebox.showinfo("Result", "Phone number must be exactly 10 digits and contain only digits")
            return False
        
        if not re.match(r"^\d{6}$", self.gui.pinCode.get()):
            messagebox.showinfo("Result", "Pin code must be 6 digits and contain only digits")
            return False

        dob_pattern = re.compile(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/\d{4}$")
        if not dob_pattern.match(self.gui.dob.get()):
            messagebox.showinfo("Result", "DOB must be in DD/MM/YYYY format")
            return False
        
        user = self.db.collection.find_one({"Vid": vid})
        if user:
            messagebox.showinfo("Result", "Vid is already registered")
            return False

        return True

    def generate_dataset(self):
        try:
            if not self.validate_fields():
                return

            myresult = self.db.collection.find()
            user_id = self.db.collection.count_documents({}) + 1

            user_data = {
                "_id": user_id,
                "Name": self.gui.name.get(),
                "DOB": self.gui.dob.get(),
                "Father Name": self.gui.fatherName.get(),
                "Phone": self.gui.phone.get(),
                "Vid": self.gui.vid.get(),
                "Pin Code": self.gui.pinCode.get(),
                "State": self.gui.state.get(),
                "City": self.gui.city.get(),
                "Address": self.gui.address.get(),
            }
            self.db.collection.insert_one(user_data)
            print("from db")
            print(user_data)

            face_classifier = cv2.CascadeClassifier(
                "./haarcascade/haarcascade_frontalface_default.xml"
            )

            def face_cropped(img):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5)

                if faces == ():
                    return None
                for x, y, w, h in faces:
                    cropped_face = img[y : y + h, x : x + w]
                return cropped_face

            cap = cv2.VideoCapture(0)
            img_id = 0

            data_folder = "dataset"
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

            while True:
                ret, frame = cap.read()
                if face_cropped(frame) is not None:
                    img_id += 1
                    face = cv2.resize(face_cropped(frame), (200, 200))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    file_name_path = f"dataset/user.{user_id}.{img_id}.jpg"
                    cv2.imwrite(file_name_path, face)
                    cv2.putText(
                        face,
                        str(img_id),
                        (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                    )

                    cv2.imshow("Cropped face", face)
                    if cv2.waitKey(1) == 13 or int(img_id) == 250:
                        break

            cap.release()
            cv2.destroyAllWindows()
            print("Generating dataset completed!!!")
            messagebox.showinfo("Result", "Dataset Created")


        except Exception as e:
            print(f"Error in dataset generation: {str(e)}")
            messagebox.showinfo("Failed","Failed to create Dataset")

