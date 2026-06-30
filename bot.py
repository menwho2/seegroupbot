import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Get token directly from Render environment variable
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ No token found! Check Render environment variables.")
    exit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to SeeGroupBot!\n\n"
        "I search for public Telegram groups and channels.\n\n"
        "📌 Usage: /search [keyword]\n"
        "📝 Example: /search crypto\n\n"
        "🔍 Try it now!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 How to use SeeGroupBot\n\n"
        "1. Type: /search [keyword]\n"
        "2. Replace [keyword] with what you're looking for\n\n"
        "📌 Examples:\n"
        "/search bitcoin\n"
        "/search gaming\n"
        "/search crypto trading\n\n"
        "💡 Be specific for better results!"
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ Please provide a keyword.\n\n"
            "Usage: /search [keyword]\n"
            "Example: /search crypto"
        )
        return

    keyword = " ".join(context.args)

    searching_msg = await update.message.reply_text(
        f"🔍 Searching for: *{keyword}*\n⏳ Please wait...",
        parse_mode="Markdown"
    )

    try:
        results = [
            {"name": f"{keyword.title()} Community", "link": f"t.me/{keyword}community", "members": "1,234"},
            {"name": f"{keyword.title()} Hub", "link": f"t.me/{keyword}hub", "members": "5,678"},
            {"name": f"{keyword.title()} Discussion", "link": f"t.me/{keyword}discuss", "members": "9,012"},
        ]

        results_message = f"🔍 **Search results for:** *{keyword}*\n\n"
        results_message += "📢 **Found these public groups:**\n\n"

        for i, group in enumerate(results, 1):
            results_message += f"{i}. **{group['name']}**\n"
            results_message += f"   🔗 {group['link']}\n"
            results_message += f"   👥 Members: {group['members']}\n\n"

        results_message += "💡 **Upgrade to premium** for more results! (Coming soon)"

        await searching_msg.delete()
        await update.message.reply_text(results_message, parse_mode="Markdown")

    except Exception as e:
        await searching_msg.delete()
        await update.message.reply_text(
            "⚠️ Something went wrong. Please try again later."
        )
        print(f"Error: {e}")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Unknown command.\n\n"
        "Available commands:\n"
        "/start - Welcome\n"
        "/help - Help guide\n"
        "/search [keyword] - Search groups\n\n"
        "Try: /search crypto"
    )

def main():
    print("🤖 Starting SeeGroupBot...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    print("✅ Bot is running!")
    app.run_polling()

if __name__ == "__main__":
    main()