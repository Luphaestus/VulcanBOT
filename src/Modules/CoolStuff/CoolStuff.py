import Helper
import Save
import asyncio
import telebot

class Module():
    def __init__(self, bot, handles):
        self.bot = bot
        self.id = "CoolStuff"
        self.only_attachments_manager = Save.json_manager("only_attachments.json")

        if "/" not in handles["prefix"]: handles["prefix"]["/"] = []
        handles["prefix"]["/"].append(["registerCoolStuff", self.only_attachments_command, self.id])
        if "" not in handles["prefix"]: handles["prefix"][""] = []
        handles["prefix"][""].append(["", self.remove_message, self.id])

    async def only_attachments_command(self, message):
           message_thread_id = message.message_thread_id
           chat_id = message.chat.id
           user_id = message.from_user.id
           if not await Helper.is_user_admin(chat_id, user_id, self.bot):
               await self.bot.delete_message(chat_id=chat_id, message_id=message.message_id)
               return
           if message_thread_id in self.only_attachments_manager.only_attachments:
               self.only_attachments_manager.remove(message_thread_id)
               reply = await self.bot.reply_to(message, "Removed message restriction\.")
           else:
               self.only_attachments_manager.add(message_thread_id)
               reply = await self.bot.reply_to(message, "Messages without attachments will be deleted\.")

           await asyncio.sleep(3)
           await self.bot.delete_message(chat_id=chat_id, message_id=message.message_id)
           await self.bot.delete_message(chat_id=reply.chat.id, message_id=reply.message_id)

    async def remove_message(self, message):

        if (message.document or message.photo):
            return
        message_thread_id = message.message_thread_id
        if message_thread_id in self.only_attachments_manager.only_attachments:
            chat_id = message.chat.id

            reply = await self.bot.reply_to(message,
                """You can only send Cool Stuff in this channel\!""",
                message_thread_id=message_thread_id)
            await asyncio.sleep(5)
            await self.bot.delete_message(chat_id=reply.chat.id, message_id=reply.message_id)
            await self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)




