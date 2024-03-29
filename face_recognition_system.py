from controllers.train_classifier import Trainer
from controllers.detect_face import FaceDetector
from controllers.generate_dataset import DatasetGenerator
from db.database import Database
from gui import FaceRecognitionGUI

class FaceRecognitionSystem:
    def __init__(self):
        self.db = Database()
        self.gui = FaceRecognitionGUI(self)
        self.trainer = Trainer()
        self.detector = FaceDetector()
        self.generator = DatasetGenerator(self.gui)

    def train_classifier(self):
        self.trainer.train_classifier()

    def detect_face(self):
        self.detector.detect_face()

    def generate_dataset(self):
        self.generator.generate_dataset()



