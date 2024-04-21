import os
from moviepy.editor import VideoFileClip
import shutil
import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MyPassword",
    database="lipReadingDB"
)
cursor = conn.cursor()

master_folder = "/Users/Usman/Documents/Projects/LipReadingPortal/data"

destination_folder = "media"

# Fetch the last inserted text data ID and word ID
cursor.execute("SELECT MAX(id) FROM lipReadingDataset_textdata;")
last_textdata_id = cursor.fetchone()[0]
if last_textdata_id is None:
    last_textdata_id = 0

cursor.execute("SELECT MAX(id) FROM lipReadingDataset_worddetail;")
last_worddetail_id = cursor.fetchone()[0]
if last_worddetail_id is None:
    last_worddetail_id = 0

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

# Function to escape single quotes in text
def escape_single_quotes(text):
    return text.replace("'", "''")

# Generate SQL INSERT queries for lipReadingDataset_textdata table
def generate_textdata_query(text_id, text, video_duration, video_link):
    text = escape_single_quotes(text)
    textdata_query = f"INSERT INTO lipReadingDataset_textdata (id, text, video_duration, video_link) VALUES ({text_id}, '{text}', {video_duration}, '/{video_link}');"
    return textdata_query

# Generate SQL INSERT queries for lipReadingDataset_worddetail table
def generate_worddetail_query(text_id, data):
    global last_worddetail_id
    worddetail_queries = []
    for item in data[2:]:
        word = escape_single_quotes(item[0])
        start_time = float(item[1])
        end_time = float(item[2])
        word_duration = round(end_time - start_time, 3)
        last_worddetail_id += 1
        worddetail_query = f"INSERT INTO lipReadingDataset_worddetail (id, word, start_time, end_time, text_id_id, word_duration, difficulty, positive, negative, pos_id_id) VALUES ({last_worddetail_id}, '{word}', '{start_time}', '{end_time}', {text_id}, {word_duration}, 'unknown', 0, 0, 1);"
        worddetail_queries.append(worddetail_query)
    return worddetail_queries

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
                    
                    # Generate SQL INSERT queries for lipReadingDataset_textdata table
                    last_textdata_id += 1
                    textdata_query = generate_textdata_query(last_textdata_id, text, video_duration, destination_video_path)
                    print(textdata_query)
                    cursor.execute(textdata_query)
                    conn.commit()
                    print("Textdata Query:", textdata_query)
                    
                    # Generate SQL INSERT queries for lipReadingDataset_worddetail table
                    worddetail_queries = generate_worddetail_query(last_textdata_id, data)
                    for query in worddetail_queries:
                        cursor.execute(query)
                        conn.commit()
                        print("Worddetail Query:", query)
                else:
                    print("No corresponding video file found.")
        else:
            print("No text files found.")

# Close the database connection
conn.close()
