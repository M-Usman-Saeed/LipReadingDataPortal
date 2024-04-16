import os
from moviepy.editor import VideoFileClip
import shutil

master_folder = "path/to/master_folder"
destination_folder = "path/to/destination_folder"

# Function to read text file and extract data
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        text = lines[0].strip().split('Text: ')[1]
        data = [line.strip().split() for line in lines[2:]]
        return text, data

# Function to calculate video duration
def calculate_video_duration(video_path):
    clip = VideoFileClip(video_path)
    duration = clip.duration
    clip.close()
    return round(duration, 3)

# Iterate through folders
for folder_name in os.listdir(master_folder):
    folder_path = os.path.join(master_folder, folder_name)
    if os.path.isdir(folder_path):
        print("Subfolder:", folder_name)
        
        # Check for text files
        text_files = [file for file in os.listdir(folder_path) if file.endswith('.txt')]
        
        if text_files:
            for index, text_file in enumerate(text_files, start=1):
                text_path = os.path.join(folder_path, text_file)
                video_file = os.path.splitext(text_file)[0] + ".mp4"  # Assuming video files have the same name as text files
                video_path = os.path.join(folder_path, video_file)
                
                # Read text file and extract data
                text, data = read_text_file(text_path)
                print("Text file:", text_file)
                print("Text:", text)
                
                # Print every word with start time, end time, and duration
                for item in data[2:]:
                    word = item[0]
                    start_time = float(item[1])
                    end_time = float(item[2])
                    duration = round(end_time - start_time, 3)
                    print("Word:", word, "Start:", start_time, "End:", end_time, "Duration:", duration)
                
                # Copy video file to destination folder if it exists
                if os.path.exists(video_path):
                    # Generate a unique name for the video file
                    video_filename = f"{folder_name}_video_{index}.mp4"
                    destination_video_path = os.path.join(destination_folder, video_filename)
                    
                    # Copy video file to destination folder
                    shutil.copy(video_path, destination_video_path)
                    
                    # Calculate video duration
                    video_duration = calculate_video_duration(destination_video_path)
                    print("Video path:", destination_video_path, "Duration:", video_duration)
                else:
                    print("No corresponding video file found.")
        else:
            print("No text files found.")
