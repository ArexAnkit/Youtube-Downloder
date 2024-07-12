import moviepy.editor as mp
from moviepy.editor import VideoFileClip

# video path
my_video = "C:\\Users\\ankit\\Downloads\\Ragada ragada 4K VIDEO SONG WITH 51 DOLBY ATMOS AUDIO.webm"

# audio path
my_audio = "C:\\Users\\ankit\\Downloads\\Ragada ragada 4K VIDEO SONG WITH 51 DOLBY ATMOS AUDIO.mp4"

# Load the video file
video = VideoFileClip(my_video)

# Get the duration in seconds
duration = video.duration
print(f"Duration: {duration} seconds")

#load vided
video = mp. VideoFileClip(my_video)

# cut from video
video = video.subclip(0, 5.56)

# add audio to video
audio = mp.AudioFileClip(my_audio) 
audio = audio.subclip(0, 5.56)

# add audio to video
new_audio = mp.CompositeAudioClip([audio])
video.audio = new_audio
video.write_videofile("C:\\Users\\ankit\\Downloads\\test.mp4")