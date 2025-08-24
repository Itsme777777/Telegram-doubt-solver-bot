import logging
import wikipedia
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Replace with your bot token
TOKEN = '7082426354:AAFUqWAqX93N3dtf3hzcw6hNdgl-XXxMxoA'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hi! Tag me with /doubt or @yourbotname followed by your question, e.g., "/doubt What is Python?"')

async def doubt(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)  # Get the question after /doubt
    if not query:
        await update.message.reply_text('Please provide a question after /doubt!')
        return
    try:
        result = wikipedia.summary(query, sentences=3)  # Fetch short Wikipedia summary
        await update.message.reply_text(result, reply_to_message_id=update.message.message_id)
    except wikipedia.exceptions.PageError:
        await update.message.reply_text('Sorry, no info found on that. Try rephrasing!')
    except Exception as e:
        await update.message.reply_text(f'Error: {str(e)}')

async def mention_handler(update: Update, context: CallbackContext) -> None:
    # Respond if mentioned with @botname in groups or DM
    if update.message.text and context.bot.name in update.message.text:
        query = update.message.text.split(context.bot.name)[1].strip()  # Extract query after mention
        if query:
            try:
                result = wikipedia.summary(query, sentences=3)
                await update.message.reply_text(result, reply_to_message_id=update.message.message_id)
            except wikipedia.exceptions.PageError:
                await update.message.reply_text('Sorry, no info found. Try rephrasing!')
            except Exception as e:
                await update.message.reply_text(f'Error: {str(e)}')
        else:
            await update.message.reply_text('What\'s your doubt? Mention me with a question!')

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("doubt", doubt))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mention_handler))  # Handle mentions

    application.run_polling()

if __name__ == '__main__':
    main()
    
