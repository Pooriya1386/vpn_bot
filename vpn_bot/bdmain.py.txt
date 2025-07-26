from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
import logging
import os

API_TOKEN = "توکن رباتت اینجا"
ADMIN_ID = 123456789  # آیدی عددی خودت

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

plans = {
    "🇳🇱 هلند": {
        "10 گیگ / ۱۵ هزار تومان": "10_15",
        "20 گیگ / ۲۵ هزار تومان": "20_25",
        "50 گیگ / ۴۵ هزار تومان": "50_45",
        "200 گیگ / ۱۲۰ هزار تومان": "200_120"
    },
    "🇳🇱+🇮🇷 هلند+ایران (تانل‌شده)": {
        "10 گیگ / ۲۵ هزار تومان": "10_25",
        "20 گیگ / ۴۰ هزار تومان": "20_40",
        "50 گیگ / ۷۵ هزار تومان": "50_75",
        "200 گیگ / ۲۲۰ هزار تومان": "200_220"
    }
}

user_payment_data = {}

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    buttons = [types.KeyboardButton(text=cat) for cat in plans]
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)
    await message.answer("سلام! لطفاً دسته‌بندی پلن موردنظر را انتخاب کن:", reply_markup=kb)

@dp.message_handler(lambda message: message.text in plans)
async def show_plan_options(message: types.Message):
    category = message.text
    buttons = [types.KeyboardButton(text=plan) for plan in plans[category]]
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)
    await message.answer("حجم مورد نظر را انتخاب کن:", reply_markup=kb)

@dp.message_handler(lambda message: any(plan in message.text for p in plans.values() for plan in p))
async def send_payment_info(message: types.Message):
    user_id = message.from_user.id
    user_payment_data[user_id] = message.text
    text = (
        "لطفاً مبلغ مربوطه را به شماره کارت زیر واریز کن:\n\n"
        "💳 6037-6975-9035-0176\n"
        "🏷 به نام: وحید مرباغی\n\n"
        "سپس رسید واریزی را به صورت عکس یا متن برای من ارسال کن."
    )
    await message.answer(text)

@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.TEXT])
async def handle_payment(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_payment_data:
        caption = f"🧾 رسید جدید\n\nپلن: {user_payment_data[user_id]}\nاز طرف: @{message.from_user.username or 'ندارد'}\nآیدی: {user_id}"

        if message.content_type == types.ContentType.PHOTO:
            await bot.send_photo(ADMIN_ID, photo=message.photo[-1].file_id, caption=caption)
        else:
            await bot.send_message(ADMIN_ID, f"{caption}\n\nمتن رسید:\n{message.text}")

        await message.reply("✅ رسید ارسال شد. منتظر تایید ادمین باش.")

@dp.message_handler(commands=["approve"])
async def approve_user(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    args = message.text.split()
    if len(args) != 2:
        await message.reply("فرمت درست: /approve user_id")
        return

    user_id = int(args[1])
    await bot.send_message(user_id, "✅ پرداخت شما تایید شد.\nدر حال ساخت کانفیگ شما هستیم...")

    # جایگزین کن با ساخت یوزر از طریق Hiddify بعد از اتصال API
    await bot.send_message(user_id, "🔗 کانفیگ شما:\n(اینجا لینک رو بذار)")

if name == "main":
    executor.start_polling(dp, skip_updates=True)
