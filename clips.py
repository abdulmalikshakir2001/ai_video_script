from clipsai import ClipFinder, Transcriber
from moviepy.video.io.VideoFileClip import VideoFileClip
from multiprocessing import Pool, cpu_count
import os
# creating clips code start==============================================================

# Define a function to process and save clips using multiprocessing
def process_clip(args):
    video_path, start_time, end_time, index = args
    with VideoFileClip(video_path) as video:
        new_clip = video.subclip(start_time, end_time)
        clip_file_path = f"./clip_{index + 1}.mp4"
        new_clip.write_videofile(
            clip_file_path,
            codec="libx264",
            preset="ultrafast",  # Use a faster preset
            threads=cpu_count()
        )
    return f"Clip {index + 1} saved: Start Time: {start_time}, End Time: {end_time}"

# Create the transcriber and clipfinder instances
transcriber = Transcriber()
clipfinder = ClipFinder()

# Transcribe the audio from the video file
transcription = transcriber.transcribe(audio_file_path="./ai_python.mp4")

# Find the clips from the transcription
clips = clipfinder.find_clips(transcription=transcription)

# Filter out clips longer than 90 seconds
filtered_clips = [
    clip for clip in clips if (clip.end_time - clip.start_time) <= 90
]

# Prepare arguments for multiprocessing
clip_args = [
    ("./ai_python.mp4", clip.start_time, clip.end_time, i)
    for i, clip in enumerate(filtered_clips)
]

# Use multiprocessing Pool for parallel processing
with Pool(processes=cpu_count()) as pool:
    results = pool.map(process_clip, clip_args)

# Output the results
for result in results:
    print(result)
# creating clips code end==============================================================




    # resizing code start ==========================
    from clipsai import resize, MediaEditor, VideoFile, AudioVideoFile

# Set the file path and other variables
video_file_path = "/content/clip_1.mp4"
output_file_path = "/content/clip_1_cropped.mp4"
pyannote_auth_token = "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"  # Replace with your actual token

# Perform the cropping operation
crops = resize(
    video_file_path=video_file_path,
    pyannote_auth_token=pyannote_auth_token,
    aspect_ratio=(9, 16)  # Adjusted to 16:9 aspect ratio
)

print("Crops: ", crops.segments)

# Initialize the MediaEditor
media_editor = MediaEditor()

# Determine the type of media file
media_file = AudioVideoFile(video_file_path)  # Assuming the file contains both audio and video streams

# Resize and save the cropped video
resized_video_file = media_editor.resize_video(
    original_video_file=media_file,
    resized_video_file_path=output_file_path,  # The output file path
    width=crops.crop_width,
    height=crops.crop_height,
    segments=crops.to_dict()["segments"],
)

print("Resized video saved to:", output_file_path)

    # resizing code end ==========================
