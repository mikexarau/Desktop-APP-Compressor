import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import *
from PIL import Image
import os
from moviepy.editor import VideoFileClip
from comprimirpdf import compress as comprimir_pdf

def compress_file(file_path):
    # file_path = filedialog.askopenfilename()
    if file_path:
        file_name, file_extension = os.path.splitext(file_path)
        save_path = f"{file_name}-compressed{file_extension}"
        if file_extension.lower() in [".jpg", ".jpeg", ".png"]:
            image = Image.open(file_path)
            scale = scale_slider.get()
            width, height = image.size
            new_width = ipint(width * scale / 100)
            new_height = int(height * scale / 100)
            new_image = image.resize((new_width, new_height))
            new_image.save(save_path, optimize=True, quality=quality_slider.get())
        elif file_extension.lower() in [".mp4", ".avi", ".mov"]:
            video = VideoFileClip(file_path)
            audio_clip = video.audio
            scale = scale_slider.get()
            new_width = int(video.w * scale / 100)
            new_height = int(video.h * scale / 100)
            new_video = video.resize(width=new_width, height=new_height)
            new_video = new_video.set_audio(video.audio)
            
            # Agregar el audio al vídeo comprimido
            new_video.audio = audio_clip
            
            if file_extension.lower() == ".mov":
                save_path = f"{file_name}-compressed.mp4"
                
            new_video.write_videofile(save_path)
        elif file_extension.lower() == ".pdf":
            compress_quality = quality_slider.get()
            compress_quality //= 25 # convert quality from range (1-95) to range (0-3) for compress_pdf function
            comprimir_pdf(file_path, save_path, compress_quality)

        print(f"File saved at {save_path}")

def drop(event):
    if event.data:
        file_paths = root.tk.splitlist(event.data)
        for file_path in file_paths:
            compress_file(file_path)
        # return event.action

def on_select():
    file_paths = filedialog.askopenfilenames()
    for file_path in file_paths:
        compress_file(file_path)

def on_drag_enter(event):
    print("on_drag_enter called")
    root.configure(bg="lightblue")

def on_drag_leave(event):
    root.configure(bg="white")

root = TkinterDnD.Tk()

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)
root.dnd_bind('<<DragEnter>>', on_drag_enter)
root.dnd_bind('<<DragLeave>>', on_drag_leave)

# drop_target = DropTarget(root)
# drop_target.dnd_bind('<<Drop>>', drop)
 
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