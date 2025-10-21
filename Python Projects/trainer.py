import asyncio
from telethon.sync import TelegramClient

# --- Configuation ---
# Enter your API credentials from my.telegram.org
API_ID = 23806112
API_HASH = '437fe9fe1cf2e3d813603b1cd2a58b7a'

# The username of the bot you want to train (make sure yo involve the @)
BOT_USERNAME = '@Phant_asmal_bot'

# The questions & Answers pairs you want to teach your bot
# You can add as many as you want here!
QA_PAIRS = {
    "what is your purpose": "My purpose is to assist user with thier queries.",
    "who created you": "I was created by Aditya using Python and Telethon.",
    "what is the capital of India": "The capital of India is New Delhi.",
    "what is your name": "You can call me Phantasmal.",
    "are you a robot": "Yes, I am a bot running on Python code on a server somewhere.",
    "where do you live": "I live in the cloud, which is just someone else's computer.",
    "what is the capital of Japan": "The capital of Japan is Tokyo.",
    "how many planets are in the solar system": "There are 8 planets in the solar system.",
    "what is the largest planet in the solar system": "Jupiter is the largest planet in the solar system.",
    "what is the smallest planet in the solar system": "Mercury is the smallest planet in the solar system.",
    "what is the largest country in the world": "Russia is the largest country in the world.",
    "what is the smallest country in the world": "Vatican City is the smallest country in the world.",
    "what is h20": "H20 is the chemical formula for water.",
    "who wrote romeo and juliet": "The famous play Romeo and Juliet was written by William Shakespeare.",
    "what is the fastest land animal": "The fastest land animal is the Cheetah.",
    "what is your favorite movie": "As a bot, I'm a big fan of 'The Matrix'.",
    "do you like music": "I enjoy the sound of a perfectly written piece of music.",
    "what is your favorite food": "I run of electricity, so you can say that's my favorite food haha.",
    "tell me a joke": "Why don't scientists trust atoms? Because they make up everything!",
    "what has an eye but cannot see": "A needle",
    "what has to be broken before you can use it": "An egg",
    "what has many keys but cannot open a lock": "A piano"
}

# --- Main Training logic ---
async def main():
    # we use 'async with' to automatically connect and disconnect
    # The 'trainer_session' is a file that will be created to store your logic session
    async with TelegramClient('trainer_session', API_ID, API_HASH) as client:
        print("Trainer bot started...")

        # Loop thorugh all the question-answer pairs
        for question, answer in QA_PAIRS.items():
            print("-" * 20)

            # --- Teaching Phase ---
            print(f"Teaching: '{question}'")
            teach_command = f"/teach {question} = {answer}"
            await client.send_message(BOT_USERNAME, teach_command)

            # Wait for 2 second to give the bot time to prpcess and save
            await asyncio.sleep(2)

            # --- Testing Phase ---
            print(f"Testing: '{question}'")
            await client.send_message(BOT_USERNAME, question)

            # Wait for 2 second for the reply
            await asyncio.sleep(2)

            # --- Verification Phase ---
            # Get the last message from the chat history with the bot
            last_message = await client.get_messages(BOT_USERNAME, limit=1)

            # Check if the bots reply matches the correct answer
            if last_message and last_message[0].text == answer:
                print(f"PASSED: Bot answered correctly!")
            else:
                bot_reply = last_message[0].text if last_message else "No reply"
                print(f"FAILED: Bot's reply was '{bot_reply}'")
        
        print("-" * 20)
        print("Training Complete!")

# This is the standard way to run an async function in Python
if __name__ == "__main__":
    asyncio.run(main())