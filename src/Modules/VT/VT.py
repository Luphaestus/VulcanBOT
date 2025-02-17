import asyncio, aiohttp
from aiohttp import FormData
import Helper
import requests, Save, random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

VIRUSTOTAL_API_KEY = "a1ab9128a622105817af5a70470135c2369e81dd7db6d312a084a759f18a10f1"



class Module():
    def __init__(self, bot, handles):
        self.bot = bot
        self.id = "VT"
        handles["document"].append(self.handle_document)

    async def check_virustotal_result(self,  scan_id, message, reply):
        url = f"https://www.virustotal.com/api/v3/analyses/{scan_id}"
        headers = {
            "x-apikey": VIRUSTOTAL_API_KEY,
            "accept": "application/json",
        }
        max_retries = 10  # Set a limit for retries
        retry_count = 0
        async with aiohttp.ClientSession() as session:
            while 1:
                async with session.get(url, headers=headers) as response:
                    print(response.status)
                    print(await response.json())
                    if response.status == 200:
                        result = await response.json()
                        status = result.get("data", {}).get("attributes", {}).get("status")
                        if status == "completed":
                            return result  # Return the full result when the analysis is completed
                    # Wait before checking again
                    await asyncio.sleep(1)  # Adjust as needed
                    retry_count += 1
                    if retry_count > 3:
                        await self.handle_document(message, reply)
                        raise TimeoutError("VirusTotal analysis did not complete in a timely manner.")

    # Function to send a file to VirusTotal
    async def send_to_virustotal(self, file_path, file_content):
        upload_url = "https://www.virustotal.com/api/v3/files"
        headers = {
            "x-apikey": VIRUSTOTAL_API_KEY,
        }
        form = FormData()
        form.add_field("file", file_content, filename=file_path)

        async with aiohttp.ClientSession() as session:
            async with session.post(upload_url, headers=headers, data=form) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    raise Exception("Failed to send the file to VirusTotal.")



    # Asynchronous handler for document messages
    async def handle_document(self, message, reply=False):
        chat_file = Save.DictStorage(f'data/{message.chat.id}.json', 'json')
        chat_data = chat_file.load()
        if "VT" not in chat_data["modules"]:
            return


        document = message.document
        file_id = document.file_id
        file_info = await self.bot.get_file(file_id)


        file_url = f"https://api.telegram.org/file/bot{self.bot.token}/{file_info.file_path}"
        print(file_url)


        # Fetch the document and send it to VirusTotal
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as response:
                if response.status == 200:
                    file_content = await response.read()  # Read the whole content
                    # Send to VirusTotal
                    reply_a = reply
                    if reply==False:
                        reply = await self.bot.reply_to(message, Helper.escape_markdown(f"*🚀 File initialized!*"))

                    virustotal_result = await self.send_to_virustotal(document.file_name, file_content)
                    print(virustotal_result)
                    if reply_a == False: self.bot.edit_message_text(message_id=reply.message_id, chat_id=reply.chat.id, text=Helper.escape_markdown(f"🚀 Analysing file.."))
                    scan_id = virustotal_result.get("data", {}).get("id", "N/A")

                    try:
                        scan_result = await self.check_virustotal_result(scan_id, message, reply)
                    except TimeoutError:
                        #await self.bot.edit_message_text(message_id=reply.message_id, chat_id=reply.chat.id, text= Helper.escape_markdown(f'⚠️🚨 Timed out :( 🚨⚠️'))
                        return

                    sha256 = scan_result['meta']['file_info']['sha256']
                    md5 = scan_result['meta']['file_info']['md5']
                    sha1 = scan_result['meta']['file_info']['sha1']
                    file_size = scan_result['meta']['file_info']['size']
                    analysis_date = scan_result['data']['attributes']['date']
                    analysis_status = scan_result['data']['attributes']['status']

                    # Extract statistics
                    stats = scan_result['data']['attributes']['stats']
                    malicious = stats['malicious']
                    suspicious = stats['suspicious']
                    undetected = stats['undetected']
                    harmless = stats['harmless']
                    total_engines = harmless+undetected+suspicious+malicious

                    # Extract scan results
                    results = scan_result['data']['attributes']['results']

                    if malicious > 20:
                        heading="🚨⚠️ *Malware Detected!* ⚠️🚨"
                        await self.bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
                    else:
                        heading="✅✅ *Likely not Malware* ✅✅"

                    report = f"""{heading}
    
SHA-256: {sha256}
MD5: {md5}
SHA-1: {sha1}
File Size: {file_size} bytes
Analysis Date: {analysis_date}
Status: {analysis_status}
"""
                    results = scan_result['data']['attributes']['results']

                    for engine_name, result in results.items():
                        category = result.get('category', 'N/A')
                        scan_result = result.get('result', 'None')
                        if category in ["malicious", "undetected"]:
                            report += f"{'🪲' if category == 'malicious' else '✅'} {engine_name}"
                            if category == "malicious":
                                report += f"\n╰ {scan_result}\n"
                            else:
                                report += "\n"

                            # If item is a list, add all elements to the same row
                    report+="File uploaded by @{message.from_user.username}."
                    breif = f"""{heading}

🔴 *Malicious*: {malicious}/{total_engines} ({int(malicious/total_engines*100)}%)
🟠 *Suspicious*: {suspicious}/{total_engines} ({int(suspicious/total_engines*100)}%)
⚫ *Harmless*: {harmless}/{total_engines} ({int(harmless/total_engines*100)}%)
🟢 *Undetected*: {undetected}/{total_engines} ({int(undetected/total_engines*100)}%)

File uploaded by @{message.from_user.username}.
"""
                    print(breif)
                   # markup = InlineKeyboardMarkup([[InlineKeyboardButton("More Info", callback_data="a")]])
                    await self.bot.edit_message_text(message_id=reply.message_id, chat_id=reply.chat.id, parse_mode='MarkdownV2', text=Helper.escape_markdown(breif))

                else:
                    await self.bot.reply_to(message, Helper.escape_markdown("Failed to fetch the document."))
