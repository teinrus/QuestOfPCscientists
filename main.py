
import tkinter as tk
import pygame
from PIL import Image, ImageTk, ImageSequence
import threading
import os
import imageio
from moviepy.editor import VideoFileClip
import time


# Global variables
gif_displayed = False
gif_label = None
error_image_displayed = False
selected_index = 0
play_music_thread = None  # Added to keep track of the music thread
open_windows = []
linked_windows = set()

  # Global variables
video_playing = False

def create_video_canvas(window):
    video_canvas = tk.Canvas(window, bg="black", width=window.winfo_screenwidth(), height=window.winfo_screenheight())
    video_canvas.pack()
    return video_canvas

def play_video_with_sound(video_path):
    global video_playing
    video_playing = True

    video = VideoFileClip(video_path)
    video.preview()

    pygame.quit()
    

def open_link(event):
    global video_playing, selected_index

    selected_index = link_listbox.curselection()
    if selected_index:
        selected_link = link_listbox.get(selected_index[0])
        video_filename = f"video{selected_index[0] + 1}.mp4"  # Формируем имя видеофайла
        video_path = os.path.join("video", video_filename)  # Путь к видеофайлу
        
        play_video_with_sound(video_path)

def play_video(video_path, canvas, window):
    global video_playing
    video_playing = True
    while video_playing:
        video = imageio.get_reader(video_path)

        for frame in video:
            if window.winfo_exists():
                frame_image = ImageTk.PhotoImage(Image.fromarray(frame))
                canvas.create_image(0, 0, anchor=tk.NW, image=frame_image)
                canvas.update()
            else:
                video_playing = False
                break

gif_label = None  # Add this line at the beginning, before any function definitions

def play_gif_and_music():
    global gif_displayed, error_image_displayed, play_music_thread, gif_label

    # Reset flags to allow replaying the gif
    error_image_displayed = False
    gif_displayed = False

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    gif_path = "your_gif_file.gif"  # Замените на путь к вашему файлу GIF

    # Check if gif_label already exists
    if gif_label is None or not gif_label.winfo_exists():
        gif_label = tk.Label(root)
        gif_label.pack()

    play_gif(gif_path, gif_label)

    link_listbox.place_forget()
    gif_displayed = True
    root.update_idletasks()




gif_playing = True  # Global variable to control gif playback


def play_gif(gif_path, label, delay=100):
    gif = Image.open(gif_path)
    frames = [ImageTk.PhotoImage(gif_frame) for gif_frame in ImageSequence.Iterator(gif)]

    def update(frame_number):
        nonlocal label
        if label and label.winfo_exists():  # Check if label is still present
            frame = frames[frame_number]
            label.configure(image=frame)

            # Resize the label to fit the screen
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            label.place(x=0, y=0, relwidth=1, relheight=1)

            root.after(delay, update, (frame_number + 1) % len(frames))

    update(0)
error_label = None

def show_error_image():
    global error_image_displayed, error_label

    if not error_image_displayed:
        error_image_displayed = True

        error_image_path = "your_error_image.jpg"
        error_image = Image.open(error_image_path)
        error_photo = ImageTk.PhotoImage(error_image)

        error_label = tk.Label(root, image=error_photo)
        error_label.image = error_photo
        error_label.place(x=0, y=0, relwidth=1, relheight=1)

        if gif_displayed:
            hide_gif_and_music()

def hide_gif_and_music():
    global gif_displayed, gif_playing, gif_label, error_image_displayed, error_label

    if gif_label is not None:
        gif_playing = False
        gif_label.destroy()
        gif_label = None


    link_listbox.place(x=0, y=0, relwidth=1, relheight=1)
    gif_displayed = False

    close_all_windows()

def close_all_windows():
    global open_windows, linked_windows

    for window in open_windows:
        window.destroy()
    open_windows.clear()
    linked_windows.clear()

def restart_gif_and_music(event):
    
    close_all_windows()
    play_gif_and_music()

    

def close_window(window):
    if window in linked_windows:
        window.destroy()
        open_windows.remove(window)
        linked_windows.remove(window)



def handle_enter(event):
    global gif_displayed

    if not gif_displayed:
        open_link(event)


def handle_restart (event):
    close_all_windows()
    play_gif_and_music()

def handle_up(event):
    pygame.mixer.init()
    sound_file_path = "up.mp3"  
    pygame.mixer.music.load(sound_file_path)
    pygame.mixer.music.play()
    global selected_index
    selected_index = link_listbox.curselection()
    if selected_index and selected_index[1] > 0:
        selected_index = selected_index[0] + 1
        link_listbox.select_clear(0, tk.END)
        link_listbox.select_set(selected_index)
        link_listbox.see(selected_index)
        

def handle_down(event):
            
    pygame.mixer.init()
    sound_file_path = "down.mp3" 
    pygame.mixer.music.load(sound_file_path)
    pygame.mixer.music.play()

    global selected_index
    selected_index = link_listbox.curselection()
    max_index = link_listbox.size() - 1
    if selected_index and selected_index[1] < max_index:
        selected_index = selected_index[0] + 1
        link_listbox.select_clear(0, tk.END)
        link_listbox.select_set(selected_index)
        link_listbox.see(selected_index)



def handle_space(event):
    global gif_displayed, play_music_thread, error_image_displayed

    if error_image_displayed:
        error_label.destroy()
        error_image_displayed = False
        hide_gif_and_music()
    elif gif_displayed:
        hide_gif_and_music()
    else:
        if play_music_thread and play_music_thread.is_alive():
            if open_windows:
                close_window(open_windows[-1])
            play_gif_and_music()
        else:
            play_gif_and_music()



root = tk.Tk()

root.attributes('-fullscreen', True)
root.title("Ссылки на новые окна")

font = ("ChinaCyr", 75)

link_listbox = tk.Listbox(root, width=400, font=font)
link_listbox.place(x=0, y=0, relwidth=1, relheight=1)  # Задаем начальное положение и размер листбокса

link_listbox.configure(bg="black", fg="purple", justify="center")
open_windows = []
linked_windows = set()

for i in range(1, 7):
    link_text = f"подсказка номер {i}"
    link_listbox.insert(tk.END, link_text)

link_listbox.select_set(selected_index)

root.bind('<Return>', handle_enter)
link_listbox.focus_set()

play_gif_and_music()

root.bind('<KeyPress-3>', lambda event=None: close_window(root.focus_get()))
root.bind('<KeyPress-1>', handle_space)
root.bind('<KeyPress-2>', lambda event=None: show_error_image())
root.bind('<Up>', handle_up)  # Обработка клавиши "Вверх"
root.bind('<Down>', handle_down)  # Обработка клавиши "Вниз"
root.mainloop()