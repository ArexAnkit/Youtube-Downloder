from pytube import YouTube  # Import the YouTube class from the pytube library
import os  # Import the os module to handle file paths
import tkinter as tk  # Import tkinter for GUI
from tkinter import messagebox, filedialog, scrolledtext  # Import additional tkinter widgets
import subprocess  # Import subprocess to handle terminal commands

def download_youtube_video():
    """
    This function downloads a YouTube video based on user input and returns the file name of the downloaded video.
    """
    link = link_var.get()  # Get the YouTube link from the entry widget
    if not link:
        messagebox.showerror("Error", "Please enter a YouTube link")
        return

    try:
        youtube = YouTube(link)  # Create a YouTube object using the provided link
        videos = youtube.streams.all()  # Retrieve all available streams for the video

        # Enumerate the streams and display them in the listbox
        vid_listbox.delete(0, tk.END)
        for i, stream in enumerate(videos):
            vid_listbox.insert(tk.END, f"{i}. {stream}")

        def on_select(event):
            selected_index = vid_listbox.curselection()
            if selected_index:
                strm = int(selected_index[0])
                download_path = videos[strm].download(download_dir)  # Download the selected stream
                file_name = os.path.basename(download_path)  # Extract the file name from the download path
                terminal_output.insert(tk.END, f"Successfully downloaded: {file_name}\n")
                terminal_output.see(tk.END)

        vid_listbox.bind('<<ListboxSelect>>', on_select)

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

download_button = tk.Button(root, text="Download", command=download_youtube_video)
download_button.pack(pady=20)

vid_listbox = tk.Listbox(root, width=80, height=10)
vid_listbox.pack(pady=5)

# Create a scrolled text widget for terminal-like output
terminal_output = scrolledtext.ScrolledText(root, width=80, height=10)
terminal_output.pack(pady=5)

# Start the GUI event loop
root.mainloop()
