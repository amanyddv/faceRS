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



class FaceRecognitionGUI:
    def __init__(self, system):
        self.system = system
        self.system.window = tk.Tk()
        self.system.window.title("Crime Buster")
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        print(hasattr(cv2, 'face'))

        self.clf = cv2.face.LBPHFaceRecognizer_create()

        classifier_path=("./classifier/classifier.xml")

        if os.path.exists(classifier_path):
            self.clf.read(classifier_path)
        else:
            print(f"Classifier file '{classifier_path}' does not exist.")
        self.create_notebook()
        

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.system.window)

        self.tab_about = ttk.Frame(self.notebook)
        self.tab_detect = ttk.Frame(self.notebook)
        self.tab_generate = ttk.Frame(self.notebook)
        self.tab_search = ttk.Frame(self.notebook)
        self.tab_help = ttk.Frame(self.notebook)
        self.tab_video = ttk.Frame(self.notebook)  
        self.tab_photo = ttk.Frame(self.notebook)


        self.notebook.add(self.tab_about, text="About")
        self.notebook.add(self.tab_generate, text="Generate Dataset")
        self.notebook.add(self.tab_video, text="Video Recognition")
        self.notebook.add(self.tab_photo, text="Photo Recognition")
 
        self.notebook.add(self.tab_detect, text="Detect Face")

        self.notebook.add(self.tab_search, text="Search Detail")
        self.notebook.add(self.tab_help, text="Help")


        about_tab = AboutTab(self.tab_about, self.system)
        about_tab.create_about_tab()

        
        style = ttk.Style()
        style.theme_use("clam")  
        style.configure("TNotebook.Tab", background="white", foreground="black")
        style.map("TNotebook.Tab", background=[("selected", "light steel blue"), ("active", "light steel blue")])
        
        
        self.notebook.pack(
            expand=1,
            fill="both",
        )

       
        self.create_detect_tab()
        self.create_generate_tab()
        self.create_search_tab()
        self.create_help_tab()
        self.create_video_tab()
        self.create_photo_tab()
            
    def recognize_faces_in_video(self, video_path):
        cap = cv2.VideoCapture(video_path)

        while True:
            ret, frame = cap.read()

            if not ret:
                break 

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in faces:
                face_roi = gray_frame[y:y + h, x:x + w]

                label, confidence = self.clf.predict(face_roi)

                user = self.system.db.collection.find_one({"_id": label})
                user_name = user["Vid"] if user else "UNKNOWN"

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                cv2.putText(frame, f"{user_name} ", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

            cv2.imshow("Video Face Recognitio", frame)

            if cv2.waitKey(1)==13:
                break  
        cap.release()
        cv2.destroyAllWindows()

    def create_video_tab(self):
        input_frame = ttk.Frame(self.tab_video, padding=(10, 10, 10, 10))
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ttk.Label(input_frame, text="Video Recognization", font=("Arial", 18), foreground="blue").grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        ttk.Label(input_frame, text="Select Video File:").grid(row=1, column=0, pady=(0, 5), sticky="w")
        self.video_path_entry = ttk.Entry(input_frame, width=40, state="readonly")
        self.video_path_entry.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        browse_button = ttk.Button(input_frame, text="Browse", command=self.browse_video)
        browse_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        play_button = ttk.Button(input_frame, text="Play Video", command=self.play_video)
        play_button.grid(row=3, column=0, pady=(10, 0), sticky="w")
      
    def browse_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi")])
        if file_path:
            self.video_path_entry.configure(state="normal")
            self.video_path_entry.delete(0, tk.END)
            self.video_path_entry.insert(0, file_path)
            self.video_path_entry.configure(state="readonly")

    def play_video(self):
        print("work")
        video_path = self.video_path_entry.get()
        if video_path:
            self.recognize_faces_in_video(video_path)
        else:
            messagebox.showinfo("Error", "Please select a video file.")
            
    def create_search_tab(self):
        

        ttk.Label(self.tab_search, text="Search Detail", font=("Arial", 18), foreground="blue" , padding=(10, 10, 10, 10)).grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        id_label = ttk.Label(self.tab_search, text="Enter ID:", font=("Arial", 14))
        id_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.search_id_entry = ttk.Entry(self.tab_search, width=10, font=("Arial", 12))
        self.search_id_entry.grid(row=1, column=1, padx=10, pady=5)

        result_name_label = ttk.Label(self.tab_search, text="Name:", font=("Arial", 14))
        result_name_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.result_name_var = tk.StringVar()
        result_name_display = ttk.Label(self.tab_search, textvariable=self.result_name_var, font=("Arial", 12))
        result_name_display.grid(row=2, column=1, padx=10, pady=5)

        result_dob_label = ttk.Label(self.tab_search, text="DOB:", font=("Arial", 14))
        result_dob_label.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        self.result_dob_var = tk.StringVar()
        result_dob_display = ttk.Label(self.tab_search, textvariable=self.result_dob_var, font=("Arial", 12))
        result_dob_display.grid(row=2, column=3, padx=10, pady=5)

        result_fatherName_label = ttk.Label(self.tab_search, text="Father Name:", font=("Arial", 14))
        result_fatherName_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.result_fatherName_var = tk.StringVar()
        result_fatherName_display = ttk.Label(self.tab_search, textvariable=self.result_fatherName_var, font=("Arial", 12))
        result_fatherName_display.grid(row=3, column=1, padx=10, pady=5)

        result_phone_label = ttk.Label(self.tab_search, text="Phone:", font=("Arial", 14))
        result_phone_label.grid(row=3, column=2, padx=10, pady=5, sticky="w")

        self.result_phone_var = tk.StringVar()
        result_phone_display = ttk.Label(self.tab_search, textvariable=self.result_phone_var, font=("Arial", 12))
        result_phone_display.grid(row=3, column=3, padx=10, pady=5)


        result_state_label = ttk.Label(self.tab_search, text="State:", font=("Arial", 14))
        result_state_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.result_state_var = tk.StringVar()
        result_state_display = ttk.Label(self.tab_search, textvariable=self.result_state_var, font=("Arial", 12))
        result_state_display.grid(row=4, column=1, padx=10, pady=5)

        result_city_label = ttk.Label(self.tab_search, text="City:", font=("Arial", 14))
        result_city_label.grid(row=4, column=2, padx=10, pady=5, sticky="w")

        self.result_city_var = tk.StringVar()
        result_city_display = ttk.Label(self.tab_search, textvariable=self.result_city_var, font=("Arial", 12))
        result_city_display.grid(row=4, column=3, padx=10, pady=5)


        result_address_label = ttk.Label(self.tab_search, text="Address:", font=("Arial", 14))
        result_address_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.result_address_var = tk.StringVar()
        result_address_display = ttk.Label(self.tab_search, textvariable=self.result_address_var, font=("Arial", 12))
        result_address_display.grid(row=5, column=1, padx=10, pady=5)

        result_pinCode_label = ttk.Label(self.tab_search, text="Pin Code:", font=("Arial", 14))
        result_pinCode_label.grid(row=5, column=2, padx=10, pady=5, sticky="w")

        self.result_pinCode_var = tk.StringVar()
        result_pinCode_display = ttk.Label(self.tab_search, textvariable=self.result_pinCode_var, font=("Arial", 12))
        result_pinCode_display.grid(row=5, column=3, padx=10, pady=5)

        

        btn_search = ttk.Button(
            self.tab_search,
            text="Search",
            style="TButton",
            command=self.search_detail,
        )
        btn_search.grid(row=7, column=0, columnspan=3, pady=20)

        self.notebook.pack(expand=1, fill="both")

    def search_detail(self):
        try:
            entered_id = (self.search_id_entry.get())
            user = self.system.db.collection.find_one({"Vid": entered_id})
            print(user)

            if user:
                self.result_name_var.set(f"{user['Name']}")
                self.result_address_var.set(f"{user['Address']}")
                self.result_dob_var.set(f"{user['DOB']}")
                self.result_fatherName_var.set(f"{user['Father Name']}")
                self.result_phone_var.set(f"{user['Phone']}")
                self.result_pinCode_var.set(f"{user['Pin Code']}")
                self.result_state_var.set(f"{user['State']}")
                self.result_city_var.set(f"{user['City']}")

            else:
                self.result_name_var.set("Name: Not Found")
                self.result_address_var.set("Address: Not Found")

        except ValueError:
            messagebox.showinfo('Error', 'Please enter a valid ID.')

    def create_help_tab(self):
        header_label = ttk.Label(
            self.tab_help, text="Help", font=("Arial", 18), foreground="blue"
        )
        header_label.grid(row=0, column=0, pady=(10, 20), sticky="w")

        help_content = (
            "Welcome to the  Crime Buster!\n\n"
            "This application allows you to perform the following tasks:\n"
            "- Detect Face: Click the 'Detect Face' button to start detecting faces using the camera.\n"
            "- Generate Dataset: Enter user details and click 'Generate Dataset' to capture images for training.\n"
            "- Train Classifier: Click 'Train Classifier' to train the face recognition classifier.\n"
            "- Search Detail: Enter an VID and click 'Search' to find details of a user.\n\n"
        )

        help_label = ttk.Label(
            self.tab_help, text=help_content, font=("Arial", 12), padding=(10, 5)
        )
        help_label.grid(row=1, column=0, pady=(0, 20), sticky="w")

    def create_detect_tab(self):
        header_label = tk.Label(
            self.tab_detect, text="Detect Face", font=("Arial", 18), fg="blue",bg="gainsboro",
        )
        header_label.pack(pady=10) 

        description_label = tk.Label(
            self.tab_detect,
            text="Click the button below to start detecting faces.",
            font=("Arial", 12),bg="gainsboro",
            pady=5,
        )
        description_label.pack()  

        btn_detect = tk.Button(
            self.tab_detect,
            text="Detect Face",
            font=("Arial", 14),
            bg="green",
            fg="white",
            command=self.system.detect_face,
        )
        btn_detect.pack(pady=10)  
        screen_width = self.system.window.winfo_screenwidth()
        screen_height = self.system.window.winfo_screenheight()

        button_width = 150  
        button_height = 40  

        x_position = (screen_width - button_width) // 2
        y_position = (screen_height - button_height) // 2

        btn_detect.place(x=x_position, y=y_position)

    def create_generate_tab(self):
        header_label = tk.Label(
            self.tab_generate, text="Generate Dataset", font=("Arial", 18), fg="blue",bg="gainsboro",
        )
        header_label.grid(row=0, column=0, pady=20, padx=10)

        name_label = tk.Label(self.tab_generate, text="Name:", font=("Arial", 14),bg="gainsboro")
        name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.name = tk.Entry(self.tab_generate, width=30, bd=5)
        self.name.grid(row=1, column=1, padx=10, pady=5)


        dob_label = tk.Label(self.tab_generate, text="DOB:", font=("Arial", 14),bg="gainsboro")
        dob_label.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.dob = tk.Entry(self.tab_generate, width=30, bd=5)
        self.dob.grid(row=1, column=3, padx=10, pady=5)

        fatherName_label = tk.Label(self.tab_generate, text="Father Name:", font=("Arial", 14),bg="gainsboro")
        fatherName_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.fatherName = tk.Entry(self.tab_generate, width=30, bd=5)
        self.fatherName.grid(row=2, column=1, padx=10, pady=5)
        
        phone_label = tk.Label(self.tab_generate, text="Phone:", font=("Arial", 14),bg="gainsboro")
        phone_label.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.phone = tk.Entry(self.tab_generate, width=30, bd=5)
        self.phone.grid(row=2, column=3, padx=10, pady=5)

        vid_label = tk.Label(self.tab_generate, text="Vid:", font=("Arial", 14),bg="gainsboro")
        vid_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.vid = tk.Entry(self.tab_generate, width=30, bd=5)
        self.vid.grid(row=3, column=1, padx=10, pady=5)

        pinCode_label = tk.Label(self.tab_generate, text="Pin Code:", font=("Arial", 14),bg="gainsboro")
        pinCode_label.grid(row=3, column=2, padx=10, pady=5, sticky="w")
        self.pinCode = tk.Entry(self.tab_generate, width=30, bd=5)
        self.pinCode.grid(row=3, column=3, padx=10, pady=5)

        state_label = tk.Label(self.tab_generate, text="State:", font=("Arial", 14),bg="gainsboro")
        state_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.state = tk.Entry(self.tab_generate, width=30, bd=5)
        self.state.grid(row=4, column=1, padx=10, pady=5)

        city_label = tk.Label(self.tab_generate, text="City:", font=("Arial", 14),bg="gainsboro")
        city_label.grid(row=4, column=2, padx=10, pady=5, sticky="w")
        self.city = tk.Entry(self.tab_generate, width=30, bd=5)
        self.city.grid(row=4, column=3, padx=10, pady=5)

        address_label = tk.Label(self.tab_generate, text="Address:", font=("Arial", 14),bg="gainsboro")
        address_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.address = tk.Entry(self.tab_generate, width=30, bd=5)
        self.address.grid(row=5, column=1, padx=10, pady=5)

        btn_generate = tk.Button(
            self.tab_generate,
            text="Generate Dataset",
            font=("Arial", 14),
            bg="green",
            fg="white",
            command=self.system.generate_dataset,
        )
        btn_generate.grid(row=10, column=1, pady=10)

        btn_train_in_generate = tk.Button(
            self.tab_generate,
            text="Train Classifier",
            font=("Arial", 14),
            bg="green",
            fg="white",
            command=self.system.train_classifier,
        )
        btn_train_in_generate.grid(row=10, column=3, pady=50)
        
    def create_photo_tab(self):
        photo_frame = ttk.Frame(self.tab_photo, padding=(10, 10, 10, 10))
        photo_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ttk.Label(photo_frame, text="Photo Recognization", font=("Arial", 18), foreground="blue").grid(row=0, column=0, columnspan=2, pady=10, sticky="w")


        ttk.Label(photo_frame, text="Select Photo File:").grid(row=1, column=0, pady=(0, 5), sticky="w")
        self.photo_path_entry = ttk.Entry(photo_frame, width=40, state="readonly")
        self.photo_path_entry.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        browse_button = ttk.Button(photo_frame, text="Browse", command=self.browse_photo)
        browse_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        recognize_button = ttk.Button(photo_frame, text="Recognize Photo", command=self.recognize_photo)
        recognize_button.grid(row=3, column=0, pady=(10, 0), sticky="w")

    def browse_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.photo_path_entry.configure(state="normal")
            self.photo_path_entry.delete(0, tk.END)
            self.photo_path_entry.insert(0, file_path)
            self.photo_path_entry.configure(state="readonly")
    
    def recognize_photo(self):
        photo_path = self.photo_path_entry.get()

        if photo_path:
            image = cv2.imread(photo_path)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in faces:
                face_roi = gray_image[y:y + h, x:x + w]
                label, confidence = self.clf.predict(face_roi)

                user = self.system.db.collection.find_one({"_id": label})
                user_name = user["Vid"] if user else "UNKNOWN"

                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 2)
                cv2.putText(image, f"{user_name}", (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

            cv2.imshow("Photo Face Recognition", image)
            cv2.waitKey(0)  
            cv2.destroyAllWindows()

        else:
            messagebox.showinfo("Error", "Please select a photo file.")

    def update_status(self, message):
        self.status_label.config(text=message)
        print(message)
