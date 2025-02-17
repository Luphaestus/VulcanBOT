import Helper
import Save
import asyncio
import telebot
import hashlib
import base64
import re
from datetime import datetime, timedelta
from math import floor as flooring

def hash_to_alphanumeric(input_string):
    print("Generating code from: ", input_string)
    # Create a SHA-256 hash of the input string
    hash_object = hashlib.sha256(input_string.encode())
    # Get the hexadecimal representation of the hash
    hash_hex = hash_object.hexdigest()
    # Convert the hex to bytes
    hash_bytes = bytes.fromhex(hash_hex)
    # Encode the bytes to base64
    base64_encoded = base64.urlsafe_b64encode(hash_bytes).decode('utf-8')
    
    # Filter to keep only alphanumeric characters
    alphanumeric = re.sub(r'[^a-zA-Z0-9]', '', base64_encoded)
    
    # Return the first 8 characters, ensuring it's alphanumeric
    return alphanumeric[:6]

def generate_code_and_validity(username, floor):
    # Get the current Unix time
    current_time = int(datetime.now().timestamp())
    
    # Round the current time to the nearest floor value
    rounded_time = flooring(current_time / floor) * floor
    
    # Generate the 8-character code
    code = hash_to_alphanumeric(username.lower() + str(rounded_time))
    
    # Set validity period (for example, 1 hour)
    validity_duration = 3600  # 1 hour in seconds
    valid_until = rounded_time + validity_duration
    
    return code, valid_until


class Module():
    def __init__(self, bot, handles):
        self.bot = bot
        self.id = "Auth"
        handles["prefix"]["/"].append(["start", self.start, self.id])
    async def start(self, message):
        if message.chat.type == "private":
            if "Auth" in message.text:
             username = message.from_user.username
             floor = 3600  # Round to the nearest second
             code, valid_until = generate_code_and_validity(username, floor)

            response_message = f"""
*Validation Code:* `{code}`
*Valid Until:* `{datetime.fromtimestamp(valid_until).strftime('%Y-%m-%d %H:%M:%S')}` (UTC)
*Epoch:* {valid_until-3600}
"""
            await self.bot.reply_to(message, response_message, parse_mode='Markdown')


