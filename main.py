import os
import tkinter as tk
import ttkbootstrap as ttk

from tkinter import filedialog
from PIL import Image, ImageTk
from time import sleep

import base64
from io import BytesIO
from icon_data import icon_data_base64


class IconMaker(ttk.Window):
    def __init__(self):
        super().__init__()
        # Icon
        icon_binary = base64.b64decode(icon_data_base64)
        icon_stream = BytesIO(icon_binary)
        icon_image = Image.open(icon_stream)
        icon = ImageTk.PhotoImage(icon_image)
        # icon = tk.PhotoImage(file="app_icon_64.png")
        self.iconphoto(True, icon)

        # Title
        self.title("Icon Maker")
        self.font = ("Helvetica", 14)
        self.SIZE = 200, 200

        # Image Selection
        self.imput_image_frame = ttk.Frame(master=self)
        self.label_image = tk.Label(
            self.imput_image_frame, text="Image", font=self.font
        )
        self.label_image.pack(side="left", padx=5, pady=5, fill="both", expand=True)
        self.entry_image_path_str = tk.StringVar()
        self.entry_image_path = tk.Entry(
            self.imput_image_frame,
            font=self.font,
            state="readonly",
            textvariable=self.entry_image_path_str,
            width=50,
        )
        self.entry_image_path.pack(
            side="left", padx=5, pady=5, fill="both", expand=True
        )
        self.btn_select_image = tk.Button(
            self.imput_image_frame,
            text="Browse",
            font=self.font,
            command=self.select_image,
        )
        self.btn_select_image.pack(side="left", padx=5, pady=5)
        self.imput_image_frame.pack(fill="both", expand=True)

        # Directory Selection
        self.input_directory_frame = ttk.Frame(master=self)
        self.label_directory = tk.Label(
            self.input_directory_frame, text="Output", font=self.font
        )
        self.label_directory.pack(side="left", padx=5, pady=5, fill="both", expand=True)
        self.entry_directory_path_str = tk.StringVar()
        self.entry_directory_path = tk.Entry(
            self.input_directory_frame,
            font=self.font,
            state="readonly",
            textvariable=self.entry_directory_path_str,
            width=50,
        )
        self.entry_directory_path.pack(
            side="left", padx=5, pady=5, fill="both", expand=True
        )
        self.btn_select_directory = tk.Button(
            self.input_directory_frame,
            text="Browse",
            font=self.font,
            command=self.select_output_folder,
        )
        self.btn_select_directory.pack(side="left", padx=5, pady=5)
        self.input_directory_frame.pack(fill="both", expand=True)

        self.image_frame = ttk.Frame(master=self)

        self.image_preview_frame = tk.LabelFrame(
            master=self.image_frame, text="Image Preview:", font=self.font
        )
        # Image Preview
        self.image_preview = ttk.Canvas(self.image_preview_frame, width=200, height=200)
        self.image_preview.pack(side="left")
        self.image_preview_frame.pack(side="left", padx=5)

        self.image_info_frame = tk.LabelFrame(
            master=self.image_frame, text="Image info:", font=self.font, width=200
        )
        # Info Label
        self.name_label = ttk.Label(
            self.image_info_frame, text="Name:", font=self.font, justify="left"
        )
        self.name_label.pack(side="top", pady=5, fill="both", expand=True)
        self.size_label = ttk.Label(
            self.image_info_frame, text="Size:", font=self.font, justify="left"
        )
        self.size_label.pack(side="top", pady=5, fill="both", expand=True)
        self.type_label = ttk.Label(
            self.image_info_frame, text="Type:", font=self.font, justify="left"
        )
        self.type_label.pack(side="top", pady=5, fill="both", expand=True)
        self.res_label = ttk.Label(
            self.image_info_frame, text="Resolution:", font=self.font, justify="left"
        )
        self.res_label.pack(side="top", pady=5, fill="both", expand=True)
        self.image_info_frame.pack(side="left", padx=5, fill="both", expand=True)

        self.image_frame.pack(fill="both", expand=True)

        self.buttons_frame = ttk.Frame(master=self)
        # Generate Button
        self.generate_btn = tk.Button(
            self.buttons_frame,
            text="Generate",
            font=self.font,
            command=self.generate_icons,
            width=10,
        )
        self.generate_btn.pack(side="left", pady=10, expand=True)

        # Clear Button
        self.clear_btn = tk.Button(
            self.buttons_frame,
            text="Clear",
            font=self.font,
            command=self.clear_fields,
            width=10,
        )
        self.clear_btn.pack(side="left", pady=10, expand=True)

        self.buttons_frame.pack(fill="both", expand=True)

        self.log_frame = tk.LabelFrame(master=self, text="Log:", font=self.font)
        # Output Log
        self.output_log = tk.Text(
            self.log_frame, height=10, width=50, font=("Helvetica", 12)
        )
        # Tags for text color
        self.output_log.tag_configure("red", foreground="red")
        self.output_log.tag_configure("green", foreground="green")
        self.output_log.tag_configure("blue", foreground="blue")
        self.output_log.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))
        self.output_log.pack(pady=10, fill="both", expand=True)
        self.log_frame.pack(pady=10, fill="both", expand=True)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=(
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*"),
            ),
        )

        if not (file_path.lower().endswith((".jpg", ".jpeg", ".png"))):
            self.output_log.insert(
                tk.END, f"Unsupported file format: {file_path.split('.')[-1]} \n", "red"
            )
            return

        # Update image path
        self.entry_image_path_str.set(file_path)

        # Extract the image information
        self.image = Image.open(file_path)
        name = file_path.split("/")[-1]
        size = self.image.size  #  (width, height)
        image_format = self.image.format
        resolution = self.image.info.get(
            "dpi"
        )  # Get the image resolution (dots per inch)

        # Display the extracted information
        self.name_label.config(text=f"Name: {name}")
        self.size_label.config(text=f"Size: {size}")
        self.type_label.config(text=f"Format: {image_format}")
        self.res_label.config(text=f"Resolution: {resolution}")

        # Update the log:
        self.output_log.insert(tk.END, "Image loaded successfully \n", "green")
        self.output_log.insert(tk.END, "Name: ", "bold")
        self.output_log.insert(tk.END, f"{name}\t")
        self.output_log.insert(tk.END, "Size: ", "bold")
        self.output_log.insert(tk.END, f"{size}\t")
        self.output_log.insert(tk.END, "Format: ", "bold")
        self.output_log.insert(tk.END, f"{image_format}\t")
        self.output_log.insert(tk.END, "Resolution: ", "bold")
        self.output_log.insert(tk.END, f"{resolution}\t dpi")

        # Preview image
        self.image.thumbnail(self.SIZE)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_preview.create_image((100, 100), image=self.photo)

    def select_output_folder(self):
        output_dir_path = filedialog.askdirectory(title="Select Output Directory")
        if output_dir_path:
            self.entry_directory_path_str.set(output_dir_path)
            self.output_log.insert(tk.END, "Directory selected \n", "green")

    def generate_icons(self):
        icon_name = "ic_launcher"

        image_path = self.entry_image_path_str.get()
        output_dir = self.entry_directory_path_str.get()

        sizes = {
            "mipmap-hdpi/": (72, 72),
            "mipmap-mdpi/": (48, 48),
            "mipmap-xhdpi/": (96, 96),
            "mipmap-xxhdpi/": (144, 144),
            "mipmap-xxxhdpi/": (192, 192),
        }

        for sub_path, size in sizes.items():
            output_dir_path = f"{output_dir}/{sub_path}"
            image = Image.open(image_path)
            image = image.resize(size)
            if not os.path.exists(output_dir_path):
                os.makedirs(output_dir_path)
                self.output_log.insert(
                    tk.END, f"Output directory '{output_dir_path}' created.\n"
                )
            image.save(f"{output_dir_path}{icon_name}.png")
            image.close()
            sleep(0.1)

    def clear_fields(self):
        self.entry_image_path_str.set("")
        self.entry_directory_path_str.set("")
        self.image_preview.pack_forget()
        self.name_label.config(text="Name:")
        self.size_label.config(text="Size:")
        self.type_label.config(text="Format:")
        self.res_label.config(text="Resolution:")


if __name__ == "__main__":
    app = IconMaker()
    app.mainloop()
