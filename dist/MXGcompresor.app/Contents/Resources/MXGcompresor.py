import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os
from moviepy.editor import VideoFileClip
from comprimirpdf import compress as comprimir_pdf

def compress_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name, file_extension = os.path.splitext(file_path)
        save_path = f"{file_name}-compressed{file_extension}"
        if file_extension.lower() in [".jpg", ".jpeg", ".png"]:
            image = Image.open(file_path)
            scale = scale_slider.get()
            width, height = image.size
            new_width = int(width * scale / 100)
            new_height = int(height * scale / 100)
            new_image = image.resize((new_width, new_height))
            new_image.save(save_path, optimize=True, quality=quality_slider.get())
        elif file_extension.lower() in [".mp4", ".avi", ".mopip3 install v"]:
            video = VideoFileClip(file_path)
            scale = scale_slider.get()
            new_width = int(video.w * scale / 100)
            new_height = int(video.h * scale / 100)
            new_video = video.resize(width=new_width, height=new_height)
            new_video.write_videofile(save_path)
        elif file_extension.lower() == ".pdf":
            compress_quality = quality_slider.get()
            compress_quality //= 25 # convert quality from range (1-95) to range (0-3) for compress_pdf function
            comprimir_pdf(file_path, save_path, compress_quality)
        
        print(f"File saved at {save_path}")


root = tk.Tk()
 
scale_label = tk.Label(root, text="Scale (percentage):")
scale_label.pack()

scale_slider = tk.Scale(root, from_=1, to=100, orient=tk.HORIZONTAL)
scale_slider.set(50)
scale_slider.pack()

quality_label = tk.Label(root, text="Quality (1-95):")
quality_label.pack()

quality_slider = tk.Scale(root, from_=1, to=95, orient=tk.HORIZONTAL)
quality_slider.set(85)
quality_slider.pack()

compress_button = tk.Button(root, text="Compress File", command=compress_file)
compress_button.pack()

root.mainloop()