from pytube import YouTube  # Import the YouTube class from the pytube library
import os  # Import the os module to handle file paths
import tkinter as tk  # Import tkinter for GUI
from tkinter import messagebox, filedialog, scrolledtext, ttk  # Import additional tkinter widgets
import moviepy.editor as mp  # Import moviepy for video and audio editing
import threading  # Import threading to handle tasks in separate threads

def download_youtube_video():
    """
    This function downloads a YouTube video and audio based on user input and returns the file names of the downloaded video and audio.
    """
    link = link_var.get()  # Get the YouTube link from the entry widget
    if not link:
        messagebox.showerror("Error", "Please enter a YouTube link")
        return

    try:
        youtube = YouTube(link)  # Create a YouTube object using the provided link
        video_stream = youtube.streams.filter(only_video=True).first()  # Get the first video-only stream
        audio_stream = youtube.streams.filter(only_audio=True).first()  # Get the first audio-only stream

        # Update progress bar
        progress_bar['value'] = 0
        progress_label.config(text="Downloading video...")
        root.update_idletasks()

        # Download the video stream
        video_path = video_stream.download(download_dir)
        progress_bar['value'] = 50
        progress_label.config(text="Downloading audio...")
        root.update_idletasks()

        # Download the audio stream
        audio_path = audio_stream.download(download_dir)
        progress_bar['value'] = 75
        progress_label.config(text="Combining video and audio...")
        root.update_idletasks()

        # Extract file names
        video_file_name = os.path.basename(video_path)
        audio_file_name = os.path.basename(audio_path)

        # Display success messages
        terminal_output.insert(tk.END, f"Successfully downloaded video: {video_file_name}\n")
        terminal_output.insert(tk.END, f"Successfully downloaded audio: {audio_file_name}\n")
        terminal_output.see(tk.END)

        # Combine video and audio
        combine_video_audio(video_path, audio_path)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def combine_video_audio(video_path, audio_path):
    """
    This function combines the downloaded video and audio into a single file using moviepy.
    """
    try:
        # Load the video file
        video = mp.VideoFileClip(video_path)

        # Load the audio file
        audio = mp.AudioFileClip(audio_path)

        # Combine the audio with the video
        video = video.set_audio(audio)

        # Define the output path
        output_path = os.path.join(download_dir, "combined_output.mp4")

        # Write the final video file
        video.write_videofile(output_path)

        # Display success message
        terminal_output.insert(tk.END, f"Successfully combined video and audio into: {output_path}\n")
        terminal_output.see(tk.END)

        # Update progress bar
        progress_bar['value'] = 100
        progress_label.config(text="Completed")
        root.update_idletasks()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_directory():
    """
    This function opens a dialog to select the download directory.
    """
    global download_dir
    download_dir = filedialog.askdirectory()
    if download_dir:
        dir_label.config(text=f"Download Directory: {download_dir}")

def start_download_thread():
    """
    This function starts the download process in a separate thread.
    """
    download_thread = threading.Thread(target=download_youtube_video)
    download_thread.start()

# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# Create and place the widgets
link_label = tk.Label(root, text="YouTube Link:")
link_label.pack(pady=5)

link_var = tk.StringVar()
link_entry = tk.Entry(root, textvariable=link_var, width=50)
link_entry.pack(pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_directory)
browse_button.pack(pady=5)

dir_label = tk.Label(root, text="Download Directory: Not selected")
dir_label.pack(pady=5)

download_button = tk.Button(root, text="Download", command=start_download_thread)
download_button.pack(pady=20)

vid_listbox = tk.Listbox(root, width=80, height=10)
vid_listbox.pack(pady=5)

# Create a scrolled text widget for terminal-like output
terminal_output = scrolledtext.ScrolledText(root, width=80, height=10)
terminal_output.pack(pady=5)

# Create a progress bar
progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
progress_bar.pack(pady=5)

# Create a label for progress status
progress_label = tk.Label(root, text="")
progress_label.pack(pady=5)

# Start the GUI event loop
root.mainloop()
