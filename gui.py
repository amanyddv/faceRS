# gui.py
import os
import cv2
import numpy as np
from PIL import Image
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk


class FaceRecognitionGUI:
    def __init__(self, system):
        self.system = system
        self.system.window = tk.Tk()
        self.system.window.title("Face Recognition System")

        self.create_notebook()

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.system.window)

        # Create tabs
        self.tab_about = ttk.Frame(self.notebook)
        self.tab_detect = ttk.Frame(self.notebook)
        self.tab_generate = ttk.Frame(self.notebook)
        self.tab_search = ttk.Frame(self.notebook)
        self.tab_help = ttk.Frame(self.notebook)
        

        self.notebook.add(self.tab_about, text='About')
        self.notebook.add(self.tab_detect, text='Detect Face')
        self.notebook.add(self.tab_generate, text='Generate Dataset')
        self.notebook.add(self.tab_search, text='Search Student Detail')
        self.notebook.add(self.tab_help, text='Help')



        self.notebook.pack(expand=1, fill='both')

        # Enhance tabs
        self.create_about_tab()
        self.create_detect_tab()
        self.create_generate_tab()
        self.create_search_tab()
        self.create_help_tab()

    def create_search_tab(self):
        pass
    def create_help_tab(self):
        pass

    def create_about_tab(self):
        # Add widgets to self.tab_about to provide information about the application
        label = tk.Label(self.tab_about, text="This is an about page.")
        label.pack(padx=10, pady=10)

    def create_detect_tab(self):
        # Widgets for the Detect tab
        header_label = tk.Label(self.tab_detect, text="Detect Face", font=("Arial", 18), fg='blue')
        header_label.grid(row=0, column=0, pady=10)

        # Add Detect-specific widgets here

        # Example button for detect_face
        btn_detect = tk.Button(self.tab_detect, text="Detect Face", font=("Arial", 14), bg='green', fg='white', command=self.system.detect_face)
        btn_detect.grid(row=1, column=0, pady=10)

    def create_generate_tab(self):
        # Widgets for the Generate tab
        header_label = tk.Label(self.tab_generate, text="Generate Dataset", font=("Arial", 18), fg='blue')
        header_label.grid(row=0, column=0, pady=10)

        # Name Entry
        name_label = tk.Label(self.tab_generate, text="Name:", font=("Arial", 14))
        name_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.t1 = tk.Entry(self.tab_generate, width=30, bd=5)
        self.t1.grid(row=1, column=1, padx=10, pady=5)

        # Age Entry
        age_label = tk.Label(self.tab_generate, text="Age:", font=("Arial", 14))
        age_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.t2 = tk.Entry(self.tab_generate, width=30, bd=5)
        self.t2.grid(row=2, column=1, padx=10, pady=5)

        # Address Entry
        address_label = tk.Label(self.tab_generate, text="Address:", font=("Arial", 14))
        address_label.grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.t3 = tk.Entry(self.tab_generate, width=30, bd=5)
        self.t3.grid(row=3, column=1, padx=10, pady=5)

        # Example button for generate_dataset
        btn_generate = tk.Button(self.tab_generate, text="Generate Dataset", font=("Arial", 14), bg='pink', fg='black', command=self.system.generate_dataset)
        btn_generate.grid(row=4, column=1, pady=10)

        # Example button for train_classifier in the Generate tab
        btn_train_in_generate = tk.Button(self.tab_generate, text="Train Classifier", font=("Arial", 14), bg='orange', fg='red', command=self.system.train_classifier)
        btn_train_in_generate.grid(row=5, column=1, pady=10)

    def update_status(self, message):
        self.status_label.config(text=message)
        print(message)
