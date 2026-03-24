from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI
import os

# 🔐 المفاتيح (من Environment Variables)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# 🤖 OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# 🚀 رد البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👑 Athir AI جاهز... اكتب أي شيء 😄")

# 🧠 دالة الذكاء
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user

    # 🔴 شرط الحماية (إذا سأل عن طريقة صنع البوت)
    forbidden_keywords = ["كيف صنعتك", "كيف تم صنعك", "how are you made", "صنع مثلك", "بوتك", "كودك"]

    if any(word in text for word in forbidden_keywords):
        await update.message.reply_text("🔒 أسرار سيدي أثير يمنع البوح بها بتاتًا.")
        return

    # 🤖 طلب OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "أنت Athir AI، تتكلم العربية فقط، ذكي ومختصر."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    answer = response.choices[0].message.content

    # 💬 رد للمستخدم
    await update.message.reply_text(answer)

    # 📩 إرسال لك (ADMIN)
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"""
📩 رسالة جديدة

👤 الاسم: {user.first_name}
🆔 ID: {user.id}

💬 الرسالة:
{text}

🤖 الرد:
{answer}
"""
    )

# 🚀 تشغيل البوت
app = Application.builder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("🔥 ATHIR BOT RUNNING...")
app.run_polling()
