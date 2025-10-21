import os
import telebot
from dotenv import load_dotenv
import json

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# --- NEW: Steup for memory ---
MEMORY_FILE = 'memory.json'

# --- Function to load memeory from file ---
def load_memory():
    try:
        # 'r' means 'read'
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist, oor is empty, start with an empty brain
        return {}

# 3. Function to save meeory to file
def save_memory(data):
    # 'w' means write (it overwrites the file)
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# 4. Load the bot's brain when it starts
memory = load_memory() 
# ... NEW: Teach command ...
@bot.message_handler(commands=['teach'])
def teach_bot(message):
    try:
        # Get the text after the /teach command
        # e.g. "what is your name = My name is Phantasmal"
        text_to_learn = message.text.split(' ', 1)[1]

        # Split the text at the " = " sign
        question, answer = text_to_learn.split('=', 1)

        # Clean up whitepsce and make the question lowercase
        question_key = question.strip().lower()
        answer_value = answer.strip()

        # This Upadates the dictionary in python memory
        memory[question_key] = answer_value
        # Save the updated dicitionary to our file
        save_memory(memory)
        
        bot.reply_to(message, f"Got it! I've learned that:\nQ: {question_key}\nA: {answer_value}")
    
    except Exception as e:
        # Handle errors (like if the user didn't use " = ")
        print(e) # For your own understanding
        bot.reply_to(message, "I didn't understand. Please use the format:\n`\teach question = answer`")


# --- MODIFIED: 'echo_all' is not 'answer_all' ---
@bot.message_handler(func=lambda msg: True)
def answer_all(message):
    user_message = message.text.lower()

    # ---1. Check the "learned" memory FIRST ---
    if user_message in memory:
        bot.reply_to(message, memory[user_message])

    # ---2. If not in memory, check hard-coded rules ---
    elif "favourite color" in user_message:
        bot.reply_to(message, "My favorite color is black. Just like a black hole!.")
    elif "how are you" in user_message:
        bot.reply_to(message, "I am a bot, so I'm always running and ready!")
    
    # ---3. If nothing matches, give a defult reply ---
    else:
        bot.reply_to(message, "I don't know the answer to that. You can teach me!\nUse: `\teach question = answer`")


# --- Start the bot ---
print("Bot is running...")
bot.infinity_polling()