from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random

TOKEN = "telegram API token" 

flags = [
    {"emoji": "🇯🇵", "country": "japan"},
    {"emoji": "🇫🇷", "country": "france"},
    {"emoji": "🇩🇪", "country": "germany"},
    {"emoji": "🇳🇬", "country": "nigeria"},
    {"emoji": "🇧🇷", "country": "brazil"},
    {"emoji": "🇺🇸", "country": "usa"},
    {"emoji": "🇮🇳", "country": "india"},
    {"emoji": "🇨🇦", "country": "canada"},
    {"emoji": "🇰🇷", "country": "south korea"},
    {"emoji": "🇬🇧", "country": "uk"},
    {"emoji": "🇮🇹", "country": "italy"},  
    {"emoji": "🇲🇽", "country": "mexico"},
    {"emoji": "🇦🇺", "country": "australia"},
    {"emoji": "🇳🇿", "country": "new zealand"},
    {"emoji": "🇪🇬", "country": "egypt"},
    {"emoji": "🇿🇦", "country": "south africa"},
    {"emoji": "🇹🇷", "country": "turkey"},
    {"emoji": "🇸🇬", "country": "singapore"},
    {"emoji": "🇸🇦", "country": "saudi arabia"},
    {"emoji": "🇮🇩", "country": "indonesia"},
    {"emoji": "🇵🇰", "country": "pakistan"},
    {"emoji": "🇳🇴", "country": "norway"},
    {"emoji": "🇸🇪", "country": "sweden"},
    {"emoji": "🇫🇮", "country": "finland"},
    {"emoji": "🇦🇷", "country": "argentina"},
    {"emoji": "🇨🇳", "country": "china"},
    {"emoji": "🇷🇺", "country": "russia"},
    {"emoji": "🇵🇭", "country": "philippines"},
    {"emoji": "🇮🇱", "country": "israel"},
    {"emoji": "🇺🇦", "country": "ukraine"},
    {"emoji": "🇹🇭", "country": "thailand"},
]

# Store game state
game_sessions = {}

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    selected_flags = random.sample(flags, 10)
    game_sessions[user_id] = {
        "flags": selected_flags,
        "score": 0,
        "current": 0
    }
    await ask_flag(update, context, user_id)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 How to Play:\n"
        "- Use /play to start the quiz.\n"
        "- You will see a flag emoji.\n"
        "- Reply with the correct country name.\n"
        "- Score is tracked, and final score is shown at the end.\n"
        "- Use /retry to play again or /quit to stop playing.\n"
        "Have fun! 🎉"
    )
    

async def ask_flag(update, context, user_id):
    game = game_sessions[user_id]
    if game["current"] < 10:
        flag = game["flags"][game["current"]]
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Guess the country for: {flag['emoji']}"
        )
    else:
        score = game["score"]
        del game_sessions[user_id]
        reply_markup = ReplyKeyboardMarkup([["Play Again", "Quit"]], one_time_keyboard=True, resize_keyboard=True)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"🎉 Game Over! You scored {score}/10.",
            reply_markup=reply_markup
        )

async def handle_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip().lower()

    if text == "play again":
        await play(update, context)
        return
    if text == "quit":
        await update.message.reply_text("Thanks for playing!", reply_markup=ReplyKeyboardRemove())
        return

    game = game_sessions.get(user_id)
    if not game:
        await update.message.reply_text("Type /play to start the game!")
        return

    current_flag = game["flags"][game["current"]]
    if text == current_flag["country"].lower():
        await update.message.reply_text("✅ Correct!")
        game["score"] += 1
    else:
        await update.message.reply_text(f"❌ Wrong! The correct answer was: {current_flag['country']}")

    game["current"] += 1
    await ask_flag(update, context, user_id)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_firstname = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 Hi {user_firstname}!\n"
        "Welcome to the Adam's Flag Guessing Game! 🌍\n\n"
        "🧠 You'll be shown a flag in emoji form, and you have to guess the country name.\n"
        "🏁 You’ll get 10 flags in total, and your score will be shown at the end!\n\n"
        "🎮 Ready to challenge your geography skills?\n"
        "👉 Type /play to begin or /help for instructions."
    )

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("play", play))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_guess))

app.run_polling()
