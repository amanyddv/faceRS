import cv2
from db.database import Database

class FaceDetector:
    def __init__(self):
        self.db = Database()

    def detect_face(self):
        try:
            faceCascade = cv2.CascadeClassifier("./haarcascade/haarcascade_frontalface_default.xml")
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read("./classifier/classifier.xml")

            video_capture = cv2.VideoCapture(0)

            while True:
                ret, img = video_capture.read()
                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                features = faceCascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

                for (x, y, w, h) in features:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 2)
                    id, pred = clf.predict(gray_image[y:y+h, x:x+w])
                    confidence = int(100 * (1 - pred / 300))
                    print(id)
                    print("id")
                    user = self.db.collection.find_one({"_id": id})
                    print(user)
                    user_name = user["Vid"] if user else "UNKNOWN"
                    
                    if confidence > 74:
                        cv2.putText(img, user_name, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
                    else:
                        cv2.putText(img, "UNKNOWN", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

                cv2.imshow("Face Detection", img)

                if cv2.waitKey(1) == 13:
                    break

            video_capture.release()
            cv2.destroyAllWindows()

        except Exception as e:
            print(f'Error in face detection: {str(e)}')


