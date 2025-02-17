from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

notes = ["Vulcan-ROM", ["ksu", "detections"], ["twrp", "data-size", ], "rules"]
note_options = {} #{"twrp": ["vbmeta"], "vbmeta": ["twrp"]}
notes_content = {"twrp": """*__Twrp Install Instructions__*

Download the tar version and in Odin put twrp in the ap slot, and vbmeta in bl slot\.

[TWRP for c1s \(Note20 5G/4G\)\.](https://twrp.me/samsung/samsunggalaxynote20.html)

[TWRP for c2s \(Note20 Ultra 5G/4G\)\.](https://twrp.me/samsung/samsunggalaxynote20ultra.html)""",

                 "Vulcan-ROM": """ __*Vulcan ROM*__

To view the latest instructions and downloads, make sure you have joined the [announcement channel](https://t.me/note20updates) and click [here](https://t.me/note20updates/42)
                """,
                 "ksu": """*__Kernel SU \- Root solution__*

⚙️ KernelSU is a root solution that is integrated directly into a kernel making it less detectable\. It's compatible with a great number of Magisk modules\.

You need to install a Kernel SU compatible kernel such as [ExtremeKernel](https://t.me/VulcanROM/28802/28897), Hk Kernel or [ThundeRStormS Kernel](https://t.me/VulcanROM/28802/28836)

You then need to install the [Kernel SU manager](https://t.me/VulcanROM/28802/29019)
""",
                 "data-size": """__*Incorrect data partition size*__

This is a Kernel SU issue that can happen after flashing a module\.

To fix this, run the following commands in termux or adb shell
```
su
ksud module shrink```""",
                }


class Module():
    def __init__(self, bot, handles):
        self.bot = bot
        self.id = "Notes"
        if "/" not in handles["prefix"]: handles["prefix"]["/"] = []
        if "#" not in handles["prefix"]: handles["prefix"]["#"] = []
        handles["prefix"]["/"].append(["notes", self.message_handler, self.id])
        handles["prefix"]["#"].append(["notes", self.message_handler, self.id])
        handles["markup"]["notes"] = self.callback_query

    async def message_handler(self, message):
        await self.bot.reply_to(message, "VulcanROM Notes", reply_markup=self.gen_markup(notes))

    def gen_markup(self, items):
        markup = InlineKeyboardMarkup()  # Create an inline keyboard
        rowcount = 0
        for item in items:
            if isinstance(item, list):
                # If item is a list, add all elements to the same row
                row = [InlineKeyboardButton(sub_item, callback_data="notes" + sub_item) for sub_item in item]
                rowcount = max(rowcount, len(row))
                markup.row(*row)  # Add the row to the markup
            else:
                rowcount = max(rowcount, 1)
                # Otherwise, add as a single button in its own row
                markup.add(InlineKeyboardButton(item, callback_data="notes" + item))
        markup.row_width = rowcount

        return markup

    async def callback_query(self, call):
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        data = call.data[5:]
        if data == "back":
            content = "VulcanROM Notes"
        else:
            content = notes_content.get(data, data + " \- TBD")

        if call.message.text != content:
            if data == "back":
                options = notes
            elif data in note_options:

                options = note_options[data].copy()
                options.append("back")
            else:
                options = ["back"]


            await self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=content,
                reply_markup=self.gen_markup(options))
        else:
            await self.bot.answer_callback_query(call.id, "Already displaying this content")
