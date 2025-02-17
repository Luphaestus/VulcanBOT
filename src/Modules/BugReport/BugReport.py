import Helper
import Save
import asyncio
import telebot

class Module():
    def __init__(self, bot, handles):
        self.bot = bot
        self.id = "BugReport"
        self.save_manager = Save.json_manager("bugreport.json")
        self.send_bug = True
        self.bugreport = ["What device do you have?",
                     "What Vulcan ROM version are you on?",
                     "Describe your problem.",
                     "Does it happen all the time, or only occasionally",
                     "What Kernel SU modules do you have?",
                     "Does it still occure after formating?"]
        self.bugformat = ""
        for question in self.bugreport:
           self.bugformat+=""+question+"\nYour answer\.\n"

        if "/" not in handles["prefix"]: handles["prefix"]["/"] = []
        handles["prefix"]["/"].append(["registerBug", self.bugAdmin, self.id])
        handles["prefix"]["/"].append(["start", self.start, self.id])
        if "" not in handles["prefix"]: handles["prefix"][""] = []
        handles["prefix"][""].append(["", self.remove_message, self.id])

    async def bugAdmin(self, message):
        message_thread_id = message.message_thread_id
        chat_id = message.chat.id
        user_id = message.from_user.id

        if not await Helper.is_user_admin(chat_id, user_id, self.bot):
            await self.bot.delete_message(chat_id=chat_id, message_id=message.message_id)
            return
        if message_thread_id in self.save_manager.only_attachments:
            self.save_manager.remove(message_thread_id)
            reply = await self.bot.reply_to(message, "Removed message restriction\.")
        else:
            self.save_manager.add(message_thread_id)
            reply = await self.bot.reply_to(message, "Messages will now need to follow bug report format\.")

        await asyncio.sleep(3)
        await self.bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        await self.bot.delete_message(chat_id=reply.chat.id, message_id=reply.message_id)

    async def start(self, message):
        if message.chat.type == "private":
            if "bug" in message.text:
               await self.bot.reply_to(message, f"""__*Vulcan ROM Bug Report*__

Please use the follow template for your bug report and post it in the Bug Report Topic\.
    
Note: The bot checks if you included the question, do not modify or remove questions\. If a question is not applicable put N/A\.
    
```
{self.bugformat}
```""")

    async def remove_message(self, message):
        if message.chat.type == "private":
            return

        message_thread_id = message.message_thread_id
        chat_id = message.chat.id



        if message_thread_id in self.save_manager.only_attachments:
            for question in self.bugreport:
                if question not in message.text:
                    await self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                    if self.send_bug:
                        self.send_bug = False
                        reply = await self.bot.send_message(chat_id,
                                                            """You can only send messages using the bug report template, make sure you do not delete or alter the questions\!""",
                                                            message_thread_id=message.message_thread_id)
                        await asyncio.sleep(15)
                        await self.bot.delete_message(chat_id=reply.chat.id, message_id=reply.message_id)
                        self.send_bug = True
                    return

            ####
            reply = await self.bot.send_message(chat_id,
                    """Please wait, We are currently migrating bug reports to github\!""",
                    message_thread_id=message.message_thread_id)
            await asyncio.sleep(15)
            await self.bot.delete_message(chat_id=reply.chat.id, message_id=reply.message_id)
            ####


            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Bug Report',
                                                        url="https://t.me/VulcanROM_bot?start=bug"))
            Save.PersistentCounter('bugreports.txt').increment()
            bugreportnum  = "Bug reports #" + str(Save.PersistentCounter('bugreports.txt').get_value())

            result = await self.bot.create_forum_topic(chat_id, bugreportnum)
            firstessage = await self.bot.send_poll(chat_id, "Do you have this problem?", ["Yes", "No"], False, message_thread_id=result.message_thread_id)
            link = f"https://t.me/VulcanROM/{firstessage.message_id}"
            #link = f"https://t.me/c/{str(chat_id)[4:]}/{firstessage.message_id}"
            await self.bot.reply_to(message, f"""The topic for this bug report can be found [here\.]({link})
If you would like to fill out a bug report, please click the button bellow\!""", reply_markup=markup)

