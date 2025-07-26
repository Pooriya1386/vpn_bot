from aiogram import Router, types, F
from config import ADMIN_ID, HIDDIFY_API_KEY, HIDDIFY_PANEL_URL

router = Router()

def register_handlers(dp):
    dp.include_router(router)

@router.message(F.text == "/start")
async def start(message: types.Message):
    await message.answer("👋 خوش آمدی! برای خرید VPN گزینه‌های زیر رو انتخاب کن.")

@router.message(F.text.contains("خرید"))
async def buy(message: types.Message):
    await message.answer("💳 لطفاً مبلغ رو به شماره کارت زیر واریز کن:\n\n6037-6975-9035-0176 به نام وحید مرباغی\n\nسپس رسید پرداخت رو ارسال کن.")

@router.message(F.photo)
async def handle_receipt(message: types.Message):
    await message.forward(ADMIN_ID)
    await message.answer("📩 رسیدت برای بررسی به ادمین ارسال شد. منتظر تایید بمون.")

@router.message(F.text.startswith("/confirm"))
async def confirm_user(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔️ فقط ادمین اجازه تایید داره.")

    parts = message.text.split()
    if len(parts) != 3:
        return await message.answer("❗️ فرمت درست: /confirm [نام کاربری] [حجم گیگ]")

    username, volume = parts[1], parts[2]

    # فراخوانی API پنل Hiddify (نمونه ساده)
    import requests
    headers = {"Hiddify-API-Key": HIDDIFY_API_KEY}
    resp = requests.get(f"{HIDDIFY_PANEL_URL}/api/v2/user/all-configs/", headers=headers)
    
    if resp.status_code == 200:
        await message.answer(f"✅ یوزر {username} ساخته شد.\n📡 کانفیگ: {resp.json()}")
    else:
        await message.answer("❌ خطا در اتصال به پنل Hiddify.")
