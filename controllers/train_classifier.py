import os
from tkinter import messagebox
import cv2
import numpy as np
from PIL import Image
from db.database import Database

class Trainer:

    def train_classifier(self):
        try:
            data_dir = "D:\major project\hfd\dataset"
            path = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
            
           
            faces = []
            ids = []

            for image in path:
                img = Image.open(image).convert('L')
                image_np = np.array(img, 'uint8')
                id = int(os.path.split(image)[1].split(".")[1])
                faces.append(image_np)
                ids.append(id)

            print("training")
            
            ids = np.array(ids)

            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces, ids)



            clf.write("./classifier/classifier.xml")
            print('Training dataset completed!!!')
            messagebox.showinfo("Result", "Training Completed")


        except Exception as e:
            print(f'Error: {str(e)}')


