import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("")
CHANNEL_USERNAME = "@jakestoresd"
ADMIN_ID = 7196224715  # غيرها بالايدي حقك

async def check_subscription(update, context):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_subscription(update, context):
        await update.message.reply_text(
            "❌ لازم تشترك في القناة أولاً:\nhttps://t.me/jakestoresd"
        )
        return

    keyboard = [
        [InlineKeyboardButton("💰 خدمات الدفع", callback_data="payments")],
        [InlineKeyboardButton("🎮 شحن الألعاب", callback_data="games")],
        [InlineKeyboardButton("🌐 تصميم وخدمات", callback_data="design")],
        [InlineKeyboardButton("✈️ سفر وتأشيرات", callback_data="travel")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🌍 مرحباً بك في Jake Store\nاختر الخدمة:",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "payments":
        await query.edit_message_text(
            "💰 خدمات الدفع:\n\n- USDT\n- Payeer\n- PayPal\n- تحويلات مالية"
        )

    elif query.data == "games":
        await query.edit_message_text(
            "🎮 شحن جميع الألعاب متوفر\n\nارسل اسم اللعبة والمبلغ"
        )

    elif query.data == "design":
        await query.edit_message_text(
            "🌐 تصميم مواقع ولوحات إعلانية\n\nارسل تفاصيل طلبك"
        )

    elif query.data == "travel":
        await query.edit_message_text(
            "✈️ تذاكر وتأشيرات\n\nارسل الدولة المطلوبة"
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Bot is running...")
app.run_polling()
