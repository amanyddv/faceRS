# train_classifier.py
import os
import cv2
import numpy as np
from PIL import Image
from db.database import Database

class Trainer:
    def __init__(self):
        self.db = Database()

    def train_classifier(self):
        try:
            data_dir = "C:/Users/Aman Yadav/Desktop/FRS/data"
            path = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
            faces = []
            ids = []

            for image in path:
                img = Image.open(image).convert('L')
                image_np = np.array(img, 'uint8')
                id = int(os.path.split(image)[1].split(".")[1])

                faces.append(image_np)
                ids.append(id)

            ids = np.array(ids)

            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces, ids)

            user_count = self.db.collection.count_documents({})

            user_id = user_count + 1

            user_data = {"_id": user_id, "Name": "", "Age": "", "Address": ""}
            self.db.collection.insert_one(user_data)

            clf.write("classifier.xml")
            print('Training dataset completed!!!')

        except Exception as e:
            print(f'Error: {str(e)}')

if __name__ == "__main__":
    trainer = Trainer()
    trainer.train_classifier()
