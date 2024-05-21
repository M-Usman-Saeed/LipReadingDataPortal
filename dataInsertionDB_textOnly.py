import os
from moviepy.editor import VideoFileClip
import shutil
import mysql.connector

positive_words = [
    "absolutely",
    "accepted",
    "acclaimed",
    "accomplish",
    "accomplishment",
    "achievement",
    "action",
    "active",
    "admire",
    "adorable",
    "adventure",
    "affirmative",
    "affluent",
    "agree",
    "agreeable",
    "amazing",
    "angelic",
    "appealing",
    "approve",
    "aptitude",
    "attractive",
    "awesome",
    "beaming",
    "beautiful",
    "believe",
    "beneficial",
    "bliss",
    "bountiful",
    "bounty",
    "brave",
    "bravo",
    "brilliant",
    "bubbly",
    "calm",
    "celebrated",
    "certain",
    "champ",
    "champion",
    "charming",
    "cheery",
    "choice",
    "classic",
    "classical",
    "clean",
    "commend",
    "composed",
    "congratulation",
    "constant",
    "cool",
    "courageous",
    "creative",
    "cute",
    "dazzling",
    "delight",
    "delightful",
    "distinguished",
    "divine",
    "earnest",
    "easy",
    "ecstatic",
    "effective",
    "effervescent",
    "efficient",
    "effortless",
    "electrifying",
    "elegant",
    "enchanting",
    "encouraging",
    "endorsed",
    "energetic",
    "energized",
    "engaging",
    "enthusiastic",
    "essential",
    "esteemed",
    "ethical",
    "excellent",
    "exciting",
    "exquisite",
    "fabulous",
    "fair",
    "familiar",
    "famous",
    "fantastic",
    "favorable",
    "fetching",
    "fine",
    "fitting",
    "flourishing",
    "fortunate",
    "free",
    "fresh",
    "friendly",
    "fun",
    "funny",
    "generous",
    "genius",
    "genuine",
    "giving",
    "glamorous",
    "glowing",
    "good",
    "gorgeous",
    "graceful",
    "great",
    "green",
    "grin",
    "growing",
    "handsome",
    "happy",
    "harmonious",
    "healing",
    "healthy",
    "hearty",
    "heavenly",
    "honest",
    "honorable",
    "honored",
    "hug",
    "idea",
    "ideal",
    "imaginative",
    "imagine",
    "impressive",
    "independent",
    "innovate",
    "innovative",
    "instant",
    "instantaneous",
    "instinctive",
    "intellectual",
    "intelligent",
    "intuitive",
    "inventive",
    "jovial",
    "joy",
    "jubilant",
    "keen",
    "kind",
    "knowing",
    "knowledgeable",
    "laugh",
    "learned",
    "legendary",
    "light",
    "lively",
    "lovely",
    "lucid",
    "lucky",
    "luminous",
    "marvelous",
    "masterful",
    "meaningful",
    "merit",
    "meritorious",
    "miraculous",
    "motivating",
    "moving",
    "natural",
    "nice",
    "novel",
    "now",
    "nurturing",
    "nutritious",
    "okay",
    "one",
    "open",
    "optimistic",
    "paradise",
    "perfect",
    "phenomenal",
    "pleasant",
    "pleasurable",
    "plentiful",
    "poised",
    "polished",
    "popular",
    "positive",
    "powerful",
    "prepared",
    "pretty",
    "principled",
    "productive",
    "progress",
    "prominent",
    "protected",
    "proud",
    "quality",
    "quick",
    "quiet",
    "ready",
    "reassuring",
    "refined",
    "refreshing",
    "rejoice",
    "reliable",
    "remarkable",
    "resounding",
    "respected",
    "restored",
    "reward",
    "rewarding",
    "right",
    "robust",
    "safe",
    "satisfactory",
    "secure",
    "seemly",
    "simple",
    "skilled",
    "skillful",
    "smile",
    "soulful",
    "sparkling",
    "special",
    "spirited",
    "spiritual",
    "stirring",
    "stunning",
    "stupendous",
    "success",
    "successful",
    "sunny",
    "super",
    "superb",
    "supporting",
    "surprising",
    "terrific",
    "thorough",
    "thrilling",
    "thriving",
    "tops",
    "tranquil",
    "transformative",
    "transforming",
    "trusting",
    "truthful",
    "unreal",
    "unwavering",
    "up",
    "upbeat",
    "upright",
    "upstanding",
    "valued",
    "vibrant",
    "victorious",
    "victory",
    "vigorous",
    "virtuous",
    "vital",
    "vivacious",
    "wealthy",
    "welcome",
    "well",
    "whole",
    "wholesome",
    "willing",
    "wonderful",
    "wondrous",
    "worthy",
    "wow",
    "yes",
    "yummy",
    "zeal",
    "zealous"
]

negative_words = [
    "abysmal",
    "adverse",
    "alarming",
    "angry",
    "annoy",
    "anxious",
    "apathy",
    "appalling",
    "atrocious",
    "awful",
    "bad",
    "banal",
    "barbed",
    "belligerent",
    "bemoan",
    "beneath",
    "boring",
    "broken",
    "callous",
    "can't",
    "clumsy",
    "coarse",
    "cold",
    "cold-hearted",
    "collapse",
    "confused",
    "contradictory",
    "contrary",
    "corrosive",
    "corrupt",
    "crazy",
    "creepy",
    "criminal",
    "cruel",
    "cry",
    "cutting",
    "damage",
    "damaging",
    "dastardly",
    "dead",
    "decaying",
    "deformed",
    "deny",
    "deplorable",
    "depressed",
    "deprived",
    "despicable",
    "detrimental",
    "dirty",
    "disease",
    "disgusting",
    "disheveled",
    "dishonest",
    "dishonorable",
    "dismal",
    "distress",
    "don't",
    "dreadful",
    "dreary",
    "enraged",
    "eroding",
    "evil",
    "fail",
    "faulty",
    "fear",
    "feeble",
    "fight",
    "filthy",
    "foul",
    "frighten",
    "frightful",
    "gawky",
    "ghastly",
    "grave",
    "greed",
    "grim",
    "grimace",
    "gross",
    "grotesque",
    "gruesome",
    "guilty",
    "haggard",
    "hard",
    "hard-hearted",
    "harmful",
    "hate",
    "hideous",
    "homely",
    "horrendous",
    "horrible",
    "hostile",
    "hurt",
    "hurtful",
    "icky",
    "ignorant",
    "ignore",
    "ill",
    "immature",
    "imperfect",
    "impossible",
    "inane",
    "inelegant",
    "infernal",
    "injure",
    "injurious",
    "insane",
    "insidious",
    "insipid",
    "jealous",
    "junky",
    "lose",
    "lousy",
    "lumpy",
    "malicious",
    "mean",
    "menacing",
    "messy",
    "misshapen",
    "missing",
    "misunderstood",
    "moan",
    "moldy",
    "monstrous",
    "naive",
    "nasty",
    "naughty",
    "negate",
    "negative",
    "never",
    "no",
    "nobody",
    "nondescript",
    "nonsense",
    "not",
    "noxious",
    "objectionable",
    "odious",
    "offensive",
    "old",
    "oppressive",
    "pain",
    "perturb",
    "pessimistic",
    "petty",
    "plain",
    "poisonous",
    "poor",
    "prejudice",
    "questionable",
    "quirky",
    "quit",
    "reject",
    "renege",
    "repellant",
    "reptilian",
    "repugnant",
    "repulsive",
    "revenge",
    "revolting",
    "rocky",
    "rotten",
    "rude",
    "ruthless",
    "sad",
    "savage",
    "scare",
    "scary",
    "scream",
    "severe",
    "shocking",
    "shoddy",
    "sick",
    "sickening",
    "sinister",
    "slimy",
    "smelly",
    "sobbing",
    "sorry",
    "spiteful",
    "sticky",
    "stinky",
    "stormy",
    "stressful",
    "stuck",
    "stupid",
    "substandard",
    "suspect",
    "suspicious",
    "tense",
    "terrible",
    "terrifying",
    "threatening",
    "ugly",
    "undermine",
    "unfair",
    "unfavorable",
    "unhappy",
    "unhealthy",
    "unjust",
    "unlucky",
    "unpleasant",
    "unsatisfactory",
    "unsightly",
    "untoward",
    "unwanted",
    "unwelcome",
    "unwholesome",
    "unwieldy",
    "unwise",
    "upset",
    "vice",
    "vicious",
    "vile",
    "villainous",
    "vindictive",
    "wary",
    "weary",
    "wicked",
    "woeful",
    "worthless",
    "wound",
    "yell",
    "yucky",
    "zero",
]

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MyPassword",
    database="lipReadingDB"
)
cursor = conn.cursor()

master_folder = "/Users/Usman/Documents/LSBU Study Material/Disertation/wetransfer_lrs2-text-data_2024-03-13_1352"



# destination_folder = "media"

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

def insert_homophone(homophone):
    cursor.execute("SELECT MAX(homophone_group_id) FROM lipReadingDataset_homophone;")
    homo_group_id = cursor.fetchone()[0] + 1
    query = f"INSERT INTO lipReadingDataset_homophone (homophone, homophone_group_id) VALUES ('{homophone}', {homo_group_id});"
    cursor.execute(query)
    conn.commit()
    cursor.execute("SELECT MAX(id) FROM lipReadingDataset_homophone;")
    homo_id = cursor.fetchone()[0]
    return homo_id

def get_homo_id(word):
    query = f"SELECT id from lipReadingDataset_homophone where homophone = '{word}';"
    cursor.execute(query)
    homo_id = cursor.fetchone()
    if homo_id is not None:
        return homo_id[0]
    else:
        return insert_homophone(word)
    
def get_word_difficulty(word):
    if len(word) <= 5:
        return 'easy'
    elif 6 <= len(word) <=9:
        return 'medium'
    else:
        return 'hard'


# Generate SQL INSERT queries for lipReadingDataset_worddetail table
def generate_worddetail_query(text_id, data):
    global last_worddetail_id
    global positive_words
    global negative_words
    worddetail_queries = []
    for item in data[2:]:
        word = escape_single_quotes(item[0])
        start_time = float(item[1])
        end_time = float(item[2])
        word_duration = round(end_time - start_time, 3)
        last_worddetail_id += 1
        homo_id = get_homo_id(word)
        word_difficulty = get_word_difficulty(word)
        positive = 1 if word.lower() in positive_words else 0
        negative = 1 if word.lower() in negative_words else 0
        worddetail_query = f"INSERT INTO lipReadingDataset_worddetail (id, word, start_time, end_time, text_id, word_duration, difficulty, positive, negative, pos_id, homophone_id) VALUES ({last_worddetail_id}, '{word}', '{start_time}', '{end_time}', {text_id}, {word_duration}, '{word_difficulty}', {positive}, {negative}, 1, {homo_id});"
        worddetail_queries.append(worddetail_query)
    return worddetail_queries

# Iterate through folders
for folder_name in os.listdir(master_folder):
    folder_path = os.path.join(master_folder, folder_name)
    if os.path.isdir(folder_path):
        # print("Subfolder:", folder_name)
        
        # Check for text files
        text_files = [file for file in os.listdir(folder_path) if file.endswith('.txt')]
        
        if text_files:
            for index, text_file in enumerate(text_files, start=1):
                text_path = os.path.join(folder_path, text_file)
                # video_file = os.path.splitext(text_file)[0] + ".mp4"  # Assuming video files have the same name as text files
                # video_path = os.path.join(folder_path, video_file)
                
                # Read text file and extract data
                text, data = read_text_file(text_path)
                
                # Copy video file to destination folder if it exists
                # if os.path.exists(video_path):
                #     # Generate a unique name for the video file
                #     video_filename = f"{folder_name}_video_{index}.mp4"
                #     destination_video_path = os.path.join(destination_folder, video_filename)
                    
                #     # Copy video file to destination folder
                #     shutil.copy(video_path, destination_video_path)
                    
                #     # Calculate video duration
                #     video_duration = calculate_video_duration(destination_video_path)
                #     # print("Video path:", destination_video_path, "Duration:", video_duration)
                    
                # Generate SQL INSERT queries for lipReadingDataset_textdata table
                video_duration = 0
                destination_video_path = ''
                last_textdata_id += 1
                textdata_query = generate_textdata_query(last_textdata_id, text, video_duration, destination_video_path)
                cursor.execute(textdata_query)
                conn.commit()
                # print("Textdata Query:", textdata_query)
                
                # Generate SQL INSERT queries for lipReadingDataset_worddetail table
                worddetail_queries = generate_worddetail_query(last_textdata_id, data)
                for query in worddetail_queries:
                    print("word querry: ", query)
                    cursor.execute(query)
                    conn.commit()
                # else:
                #     print("No corresponding video file found.")
        else:
            print("No text files found.")

# Close the database connection
conn.close()