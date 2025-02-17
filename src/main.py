from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot.util
import Save, Helper, random
import asyncio, importlib.util, os


BOT_TOKEN = PUT BOT TOKEN HERE

bot = AsyncTeleBot(BOT_TOKEN,  parse_mode='MarkdownV2')
modules=[]
Handles = {"document":[], "markup":{}, "prefix":{}}


all_items = os.listdir(os.path.dirname(__file__)+"/"+"Modules")
module_directories = [item for item in all_items if not item.startswith("_")]

for module_name in module_directories:
    module_path = f"{os.path.dirname(__file__)}/Modules/{module_name}/{module_name}.py"
    module_spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    module.Module(bot, Handles)
    modules.append(module_name)

@bot.message_handler(commands=['enable'])
async def enable_module(message):
    user_info = message.from_user
    print("---------------------------------------")
    user_details = f"User ID: {user_info.id}\nFirst Name: {user_info.first_name}\nLast Name: {user_info.last_name}\nUsername: {user_info.username}"
    print(f"User Details:\n{user_details}")
    chat_file = Save.DictStorage(f'data/{message.chat.id}.json', 'json')
    chat_data = chat_file.load()
    print(message.text)
    chat_file = Save.DictStorage(f'data/{message.chat.id}.json', 'json')
    chat_data = chat_file.load()
    if not await Helper.is_user_admin(message.chat.id, message.from_user.id, bot):
        await bot.reply_to(message, Helper.escape_markdown(random.choice(Helper.not_admin)))
        return
    if not len(message.text.split()) > 1:
        await bot.reply_to(message, Helper.escape_markdown("No module specified!"))
        return
    module_name = message.text.split()[1]

    if "modules" not in chat_data.keys():
        chat_data["modules"] = []


    if module_name in modules:
        if module_name in chat_data["modules"]:
            await bot.reply_to(message, Helper.escape_markdown(f"Module `{module_name}` already enabled."))
        else:
            chat_data["modules"].append(module_name)
            await bot.reply_to(message, Helper.escape_markdown(f"Module `{module_name}` enabled."))
            chat_file.save(chat_data)
    else:
        await bot.reply_to(message, text=Helper.escape_markdown(f"Module `{module_name}` not found."))

@bot.message_handler(commands=['disable'])
async def enable_module(message):
    user_info = message.from_user
    print("---------------------------------------")
    user_details = f"User ID: {user_info.id}\nFirst Name: {user_info.first_name}\nLast Name: {user_info.last_name}\nUsername: {user_info.username}"
    print(f"User Details:\n{user_details}")
    chat_file = Save.DictStorage(f'data/{message.chat.id}.json', 'json')
    chat_data = chat_file.load()
    print(message.text)
    if not await Helper.is_user_admin(message.chat.id, message.from_user.id, bot):
        await bot.reply_to(message, Helper.escape_markdown(random.choice(Helper.not_admin)))
        return
    if not len(message.text.split()) > 1:
        await bot.reply_to(message, Helper.escape_markdown("No module specified!"))
        return
    chat_file = Save.DictStorage(f'data/{message.chat.id}.json', 'json')
    chat_data = chat_file.load()
    module_name = message.text.split()[1]

    if "modules" not in chat_data.keys():
        chat_data["modules"] = []

    if module_name in modules:
        if module_name in chat_data["modules"]:
            chat_data["modules"].remove(module_name)
            await bot.reply_to(message, Helper.escape_markdown(f"Module `{module_name}` disabled."))
            chat_file.save(chat_data)
        else:
            await bot.reply_to(message, Helper.escape_markdown(f"Module `{module_name}` not enabled."))
    else:
        await bot.reply_to(message, text=Helper.escape_markdown(f"Module `{module_name}` not found."))

@bot.message_handler(commands=['modules'])
async def list_modules(message):
    user_info = message.from_user
    print("---------------------------------------")
    user_details = f"User ID: {user_info.id}\nFirst Name: {user_info.first_name}\nLast Name: {user_info.last_name}\nUsername: {user_info.username}"
    print(f"User Details:\n{user_details}")
    chat_file = Save.DictStorage(f'data/{message.chat.id}.json', 'json')
    chat_data = chat_file.load()
    print(message.text)

    if "modules" not in chat_data.keys():
        chat_data["modules"] = []

    result = "*Modules: \n*"
    for module in modules:
        result += f"{module} {'✅' if module in chat_data['modules'] else ''}\n"
    await bot.reply_to(message, result)


@bot.message_handler(content_types=["document"])
async def document_handler(message):
    for handle in Handles["document"]:
        await handle(message)

@bot.message_handler(func=lambda call: True)
async def message(message):
    user_info = message.from_user
    print("---------------------------------------")
    user_details = f"User ID: {user_info.id}\nFirst Name: {user_info.first_name}\nLast Name: {user_info.last_name}\nUsername: {user_info.username}"
    print(f"User Details:\n{user_details}")
    print(message.text)
    for prefix in Handles["prefix"].keys():
        if message.text.startswith(prefix):
            for module in Handles["prefix"][prefix]:

                if not check_module_status(message, module[2]): continue
                if message.text.startswith(prefix+module[0]):

                    await module[1](message)

@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    for callback in Handles["markup"].keys():
        if call.data.startswith(callback):
            await Handles["markup"][callback](call)


def check_module_status(message, id):
    chat_file = Save.DictStorage(f'data/{message.chat.id}.json', 'json')
    chat_data = chat_file.load()
    try:
        return id in chat_data["modules"]
    except:
        return True

while 1:
    try:
        print("running")
        asyncio.run(bot.polling())
    except:
        print("CRASH")
