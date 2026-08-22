import os
from dotenv import load_dotenv
from rubka import Robot, Message

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = Robot(token=TOKEN)


@bot.on_message()
async def receive_message(bot: Robot, message: Message):
    print("📩 پیام جدید دریافت شد:")
    print("متن:", message.text)


bot.run()