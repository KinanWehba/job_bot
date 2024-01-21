import logging
from telegram import  Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,)

from add_job_handler import(
    add_job , 
    regular_choice ,
    # custom_choice ,
    received_information ,
    done ,
    CHOOSING,
    TYPING_CHOICE,
    TYPING_REPLY,
    regex_pattern,
    regex_category,
    )
from helper_function import base_request
from dotenv import load_dotenv
import os
import re

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")



async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Use /cancel to stop the bot.\n"
        "Use /start to start the bot again.",)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    username = update.message.from_user.username
    fname = update.message.from_user.first_name
    lname = update.message.from_user.last_name
    chat_id = update.message.from_user.id
    dict_info = {
        "username":username,
        "fname":fname,
        "lanem":lname,
        "chat_id":chat_id,
        }
    req = base_request(dict_info,'start','str')
    if req == "new" :
        await update.message.reply_text(
            "اهلا بكم في دليلك بوت.\n"
            "لاضافة عمل اضغط على /add_job\n"
            "للبحث عن عمل اضغط على /search_job.\n"
            "اهلا بكم في دليلك بوت.\n"
            "اهلا بكم في دليلك بوت.\n"
            "Use /add_job to add .",
            )
    else : 
        await update.message.reply_text(
            "اهلا بكم في دليلك بوت.\n"
            "لاضافة عمل اضغط على /add_job\n"
            "للبحث عن عمل اضغط على /search_job.\n"
            "اهلا بكم في دليلك بوت.\n"
            "اهلا بكم في دليلك بوت.\n"
            "Use /add_job to add .",
            )

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()
    help_handler = CommandHandler("help", help)
    start_handler = CommandHandler("start", start)
    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add_job", add_job)],
        
        states={
            CHOOSING: [
                MessageHandler(filters.Regex(regex_pattern), regular_choice),
                # MessageHandler(filters.Regex("^اضافة تفصيل$"), custom_choice),
                ],
            TYPING_CHOICE: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^حفظ$")), regular_choice)],
            TYPING_REPLY: [
                CallbackQueryHandler( received_information, pattern= regex_category),
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^حفظ$")),received_information,)],
            },
        fallbacks=[MessageHandler(filters.Regex("^حفظ$"), done)],
 )

    application.add_handler(help_handler)
    application.add_handler(start_handler)
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()