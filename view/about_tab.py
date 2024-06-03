import tkinter as tk
from PIL import ImageTk, Image

class AboutTab:
    def __init__(self, tab_about, system):
        self.tab_about = tab_about
        self.system = system

    def create_about_tab(self):
        about_label = tk.Label(
            self.tab_about,
            text="Welcome to the Aadhar : A Crime Buster.\n"
            "This application allows you to perform face detection, generate datasets,\n"
            "search for criminal details, and more.",
            font=("Arial", 14),bg="gainsboro",
        )
        about_label.pack(padx=10, pady=10)

        image_path = "./assets/download.jpg"  
        screen_width = self.system.window.winfo_screenwidth()
        image = Image.open(image_path)
        image_width, image_height = image.size
        aspect_ratio = screen_width / image_width
        new_width = int(image_width * aspect_ratio)
        new_height = int(image_height * aspect_ratio)
        resized_image = image.resize((new_width, new_height))

        tk_image = ImageTk.PhotoImage(resized_image)

        image_label = tk.Label(self.tab_about, image=tk_image)
        image_label.image = tk_image
        image_label.pack(pady=10)
