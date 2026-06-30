import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ No token found!")
    exit()

async def start(update, context):
    await update.message.reply_text("👋 Welcome to SeeGroupBot! Try /help")

async def help_command(update, context):
    await update.message.reply_text("🔍 Commands: /start, /help, /search [keyword]")

async def search(update, context):
    if not context.args:
        await update.message.reply_text("❌ Please provide a keyword. Example: /search crypto")
        return
    keyword = " ".join(context.args)
    await update.message.reply_text(f"🔍 Searching for: {keyword}\n\n⏳ Coming soon!")

async def unknown(update, context):
    await update.message.reply_text("❌ Unknown command. Try /help")

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