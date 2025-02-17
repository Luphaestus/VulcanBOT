import re, aiohttp

not_admin = [
    "Looks like you're trying to access admin features. Have you tried turning yourself into an admin first? 😜",
    "Sorry, only wizards with admin wands can do that. You might want to check your inventory for a magical upgrade! 🧙‍♂️✨",
    "Admin privileges required! You might need to defeat a few more bosses to unlock this feature. 🎮",
    "Access denied! You need to level up to Admin Rank to access this area. Keep grinding! 💪",
    "Oops! It seems you're not an admin. You can try waving a magic wand, but I can't guarantee it will work! 🪄",
    "Looks like you don't have the 'Admin' badge. Don't worry; you can still enjoy the regular content! 🎉",
    "Only admins can do that. Are you sure you're in the right room? This is the 'Non-Admin' section. 🙃",
    "Hey there! You need to be an admin to do that. How about enjoying some coffee and donuts instead? ☕🍩",
    "Sorry, you don't have the admin powers to make that happen. Feel free to send your request to the 'Actual Admins' club. 😂",
    "Admin access required! If you were an admin, you’d have a cool badge. Sadly, you don’t have one. 🤷‍♂️"]


def escape_markdown(text):
    return re.sub(r'([()[\]~>#+=|{}.!\\-])', r'\\\1', text)


async def is_user_admin(chat_id, user_id, bot):
    admins = await bot.get_chat_administrators(chat_id)
    return any(admin.user.id == user_id for admin in admins)

import aiohttp
import uuid
import os
from datetime import datetime

DOWNLOAD_DIR = 'Temp'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def generate_unique_filename():
    # Create a unique identifier
    unique_id = uuid.uuid4()
    # Generate the timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    # Return the unique filename with the provided extension
    return f"{timestamp}_{unique_id}.file"

async def download_file(url):
    # Generate a unique filename
    unique_filename = generate_unique_filename()
    # Create the full path
    output_file = os.path.join(DOWNLOAD_DIR, unique_filename)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()  # Get the binary content
                # Save to file
                with open(output_file, 'wb') as f:
                    f.write(content)
                print(f"File downloaded and saved as {output_file}")
                return output_file  # Return the unique file name
            else:
                print("Failed to download the file")
                return None
