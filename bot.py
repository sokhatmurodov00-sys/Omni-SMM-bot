import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

countries = [
    ("🇺🇸 AQSH", "USA", 15000),
    ("🇨🇦 Kanada", "Canada", 17000),
    ("🇮🇩 Indoneziya", "Indonesia", 12000),
    ("🇵🇭 Filippin", "Philippines", 13000),
    ("🇰🇪 Keniya", "Kenya", 11000),
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📞 Nomer olish", callback_data="numbers")],
        [InlineKeyboardButton("💳 Mening hisobim", callback_data="balance")],
        [InlineKeyboardButton("🛒 Buyurtmalarim", callback_data="orders")],
        [InlineKeyboardButton("💵 Hisob to‘ldirish", callback_data="topup")],
        [InlineKeyboardButton("📕 Qo‘llanma", callback_data="help")],
    ]

    await update.message.reply_text(
        "🏠 ASOSIY MENYU\n\n"
        "Qonuniy xalqaro SMS qabul qilish xizmati.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "numbers":
        keyboard = []

        for name, code, price in countries:
            keyboard.append([
                InlineKeyboardButton(
                    f"{name} — {price:,} so‘m",
                    callback_data=f"country_{code}"
                )
            ])

        await query.edit_message_text(
            "🌍 Mamlakatni tanlang:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data.startswith("country_"):
        country = query.data.replace("country_", "")

        await query.edit_message_text(
            f"📞 Tanlangan davlat: {country}\n\n"
            "Buyurtma yaratish uchun xizmat mavjudligi tekshiriladi.\n"
            "SMS xizmatlari faqat qonuniy maqsadlarda ishlatiladi."
        )

    elif query.data == "balance":
        await query.edit_message_text("💳 Balansingiz: 0 so‘m")

    elif query.data == "orders":
        await query.edit_message_text("🛒 Sizda hozircha buyurtmalar yo‘q.")

    elif query.data == "topup":
        await query.edit_message_text(
            "💵 Hisob to‘ldirish\n\n"
            "To‘lov tizimi keyingi bosqichda ulanadi."
        )

    elif query.data == "help":
        await query.edit_message_text(
            "📕 Qo‘llanma\n\n"
            "1. Mamlakatni tanlang.\n"
            "2. Xizmatni buyurtma qiling.\n"
            "3. Faqat qonuniy SMS xizmatlaridan foydalaning."
        )

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN topilmadi")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()