import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, ADMIN_ID, CARD_NUMBER, CARD_NAME, SUPPORT_ID
from hiddify_api import create_user_and_get_configs

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

packages = {
    "هلند": {
        "10 گیگ، 1 ماهه": 15000,
        "20 گیگ، 1 ماهه": 25000,
        "50 گیگ، 1 ماهه": 45000,
        "200 گیگ، 1 ماهه": 120000
    },
    "هلند + ایران": {
        "10 گیگ، 1 ماهه": 25000,
        "20 گیگ، 1 ماهه": 40000,
        "50 گیگ، 1 ماهه": 75000,
        "100 گیگ، 1 ماهه": 130000,
        "200 گیگ، 1 ماهه": 220000
    }
}

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    text = (
        "سلام! 👋 به ربات فروش VPN خوش اومدی.\n\n"
        "📦 بسته‌ها:\n"
        "🇳🇱 هلند:\n" +
        "\n".join([f"- {name}: {price:,} تومان" for name, price in packages["هلند"].items()]) +
        "\n\n🇳🇱+🇮🇷 هلند+ایران:\n" +
        "\n".join([f"- {name}: {price:,} تومان" for name, price in packages["هلند + ایران"].items()]) +
        f"\n\n💳 برای خرید، مبلغ را به شماره کارت زیر واریز کن:\n\n"
        f"🏷️ به نام: {CARD_NAME}\n"
        f"💳 شماره کارت: {CARD_NUMBER}\n\n"
        "سپس رسید را ارسال کن. 📷"
    )
    await message.reply(text)

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_payment(message: types.Message):
    await bot.send_message(ADMIN_ID, f"📥 رسید جدید از {message.from_user.full_name} (@{message.from_user.username}):")
    await bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption="تأیید کن؟ ✅")

    await message.reply("✅ رسید شما دریافت شد و در حال بررسی است. تا تأیید، لطفاً صبور باشید.")

@dp.message_handler(commands=["create_user"])
async def admin_create_user(message: types.Message):
    if str(message.from_user.id) != str(ADMIN_ID):
        return await message.reply("⛔️ شما دسترسی ادمین ندارید.")

    try:
        _, name, volume_gb = message.text.split()
        link = create_user_and_get_configs(name, int(volume_gb))
        await message.reply(f"✅ یوزر ساخته شد. لینک کانفیگ:\n\n{link}")
    except Exception as e:
        await message.reply(f"❌ خطا در ساخت یوزر: {e}")

@dp.message_handler(commands=["support"])
async def support_info(message: types.Message):
    await message.reply(f"📞 برای پشتیبانی به {SUPPORT_ID} پیام دهید.")

if name == "main":
    executor.start_polling(dp, skip_updates=True)

