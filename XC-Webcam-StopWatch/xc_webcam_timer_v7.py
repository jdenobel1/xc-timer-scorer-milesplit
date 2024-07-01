import cv2
import numpy as np
import pyautogui
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import webbrowser

# Global variables for the stopwatch
start_time = None
running = False
time_str = "00:00:00.00"
recorded_times = []
txt_file_name = "times.txt"
screen_recording_file_name = "screen_record.avi"
screen_recording_thread = None
webcam_threads = []
stop_event = threading.Event()

# Function to update the stopwatch
def update_stopwatch():
    global start_time, running, time_str
    while True:
        if running:
            elapsed_time = time.time() - start_time
            hours, rem = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(rem, 60)
            hundredths = int((seconds - int(seconds)) * 100)
            time_str = "{:02}:{:02}:{:02}.{:02}".format(int(hours), int(minutes), int(seconds), hundredths)
        time.sleep(0.01)

# Function to capture video from webcam
def capture_video(device_num, window_name):
    global time_str, stop_event
    cap = cv2.VideoCapture(device_num)
    if not cap.isOpened():
        print(f"Error: Unable to open webcam {device_num}")
        return

    # Allow the window to be resizable
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Failed to read frame from webcam {device_num}")
            break

        # Get the current window size
        width = cv2.getWindowImageRect(window_name)[2]
        height = cv2.getWindowImageRect(window_name)[3]

        # Resize the frame to fit the window size
        resized_frame = cv2.resize(frame, (width, height))

        # Overlay stopwatch and webcam number on the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(resized_frame, time_str, (10, 50), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(resized_frame, f"Webcam {device_num + 1}", (10, 100), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
        cv2.imshow(window_name, resized_frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord(' '):  # Spacebar to start/stop the timer
            global running, start_time
            if running:
                running = False
            else:
                running = True
                start_time = time.time()
        elif key == ord('\r'):  # Enter key to save the time
            recorded_times.append(time_str)
            with open(txt_file_name, "a") as file:
                file.write(time_str + "\n")
            print(f"Recorded Time {len(recorded_times)} - {time_str}")

    cap.release()
    cv2.destroyWindow(window_name)

# Function to record screen
def record_screen():
    global screen_recording_file_name, stop_event
    screen = pyautogui.size()
    codec = cv2.VideoWriter_fourcc(*"XVID")
    output = cv2.VideoWriter(screen_recording_file_name, codec, 20.0, (screen.width, screen.height))

    while not stop_event.is_set():
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output.write(frame)

    output.release()
    cv2.destroyAllWindows()

# Function to start the screen recording
def start_screen_recording():
    global screen_recording_file_name, screen_recording_thread, stop_event
    stop_event.clear()
    screen_recording_file_name = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi")])
    if not screen_recording_file_name:
        messagebox.showerror("Error", "No file name provided.")
        return
    
    screen_recording_thread = threading.Thread(target=record_screen)
    screen_recording_thread.start()

# Function to stop the screen recording
def stop_screen_recording():
    global stop_event
    stop_event.set()
    if screen_recording_thread is not None:
        screen_recording_thread.join()
    messagebox.showinfo("Info", "Screen recording stopped.")

# Function to set the boys or girls time file
def set_boys_or_girls_time_file():
    global txt_file_name
    txt_file_name = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if not txt_file_name:
        messagebox.showerror("Error", "No file name provided.")
        return

# Function to start capturing video from webcams
def start_video_capture():
    global webcam_threads
    stop_event.clear()
    thread1 = threading.Thread(target=capture_video, args=(0, "Webcam 1"))
    thread2 = threading.Thread(target=capture_video, args=(1, "Webcam 2"))
    webcam_threads = [thread1, thread2]
    thread1.start()
    thread2.start()

# Function to stop capturing video from webcams
def stop_video_capture():
    global stop_event, webcam_threads
    stop_event.set()
    for thread in webcam_threads:
        thread.join()
    webcam_threads.clear()
    messagebox.showinfo("Info", "Webcam recording stopped.")

# Function to start the timer
def start_timer():
    global running, start_time
    running = True
    start_time = time.time()

# Function to stop the timer
def stop_timer():
    global running
    running = False

# Function to quit the program
def quit_program():
    global stop_event, webcam_threads
    stop_event.set()
    for thread in webcam_threads:
        thread.join()
    webcam_threads.clear()
    if screen_recording_thread is not None:
        stop_screen_recording()
    root.quit()
    root.destroy()

# Function to open XC Merged Results (xc_merge_results_v4.py)
def open_xc_merged_results():
    try:
        # Path to the executable
        exe_path = r"C:\Users\jdeno\Desktop\XC_Webcam_stopwatch\xc_merge_results_v4\xc_merge_results_v4.exe"
        
        # Check if the executable file exists
        if os.path.exists(exe_path):
            # Launch the executable
            subprocess.Popen([exe_path])
            print(f"Opened {exe_path} successfully.")
        else:
            messagebox.showerror("Error", "Executable file not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open application: {e}")

# Function to open instructions HTML file
def open_instructions():
    instructions_file = r"C:\Users\jdeno\Desktop\XC_Webcam_stopwatch\instructions.html"
    try:
        webbrowser.open_new(instructions_file)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open instructions: {e}")

# Create the main GUI
def create_gui():
    global root
    root = tk.Tk()
    root.title("Cross Country Stopwatch and Screen Recorder")

    # Instructions and Open XC Merged Results
    tk.Button(root, text="Instructions", command=open_instructions).grid(row=0, column=0, padx=20, pady=10)
    tk.Button(root, text="Open XC Merged Results", command=open_xc_merged_results).grid(row=0, column=1, padx=20, pady=10)

    # Set Boys or Girls Time File centered
    tk.Button(root, text="Set Boys or Girls Time File", command=set_boys_or_girls_time_file).grid(row=1, column=0, columnspan=2, pady=10)

    # Left column buttons
    tk.Button(root, text="Start Video Capture", command=start_video_capture).grid(row=2, column=0, padx=20, pady=10)
    tk.Button(root, text="Start Timer", command=start_timer).grid(row=3, column=0, padx=20, pady=10)
    tk.Button(root, text="Start Screen Recording", command=start_screen_recording).grid(row=4, column=0, padx=20, pady=10)

    # Right column buttons
    tk.Button(root, text="Stop Screen Recording", command=stop_screen_recording).grid(row=2, column=1, padx=20, pady=10)
    tk.Button(root, text="Stop Timer", command=stop_timer).grid(row=3, column=1, padx=20, pady=10)
    tk.Button(root, text="Stop Video Capture", command=stop_video_capture).grid(row=4, column=1, padx=20, pady=10)

    # Quit button centered at the bottom
    tk.Button(root, text="Quit", command=quit_program).grid(row=5, column=0, columnspan=2, pady=20)

    root.mainloop()

# Start the stopwatch update thread
stopwatch_thread = threading.Thread(target=update_stopwatch)
stopwatch_thread.daemon = True
stopwatch_thread.start()

# Create and run the GUI
create_gui()
