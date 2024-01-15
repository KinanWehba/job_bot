import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv
import os
import re

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)



load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
base_url = "http://127.0.0.1:5000/"
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
reply_keyboard = [
    ["Catagory"],
    ["Favourite colour"],
    ["Number of siblings"],
    ["Something else..."],
    ["Done"],
]
catagory_list = [
    ["طبيب"],
    ["استاذ"],
    ["خباز"],
]
regex_pattern = f"({'|'.join(map(re.escape, [item[0] for item in reply_keyboard[:-1] if item[0] != 'Catagory' if item[0] != 'Done' if item[0] != 'Something else...'] ))})"

# all_items = [item[0] for sublist in [reply_keyboard, catagory] for item in sublist if item[0] != 'Catagory' if item[0] != 'Done' if item[0] != 'Something else...']

# # إنشاء تعبير الاستعلام
# regex_pattern = f"({'|'.join(map(re.escape, all_items))})"



markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
markup_catagory = ReplyKeyboardMarkup(catagory_list, one_time_keyboard=True)

def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    print(facts)
    return "\n".join(facts).join(["\n", "\n"])

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Use /cancel to stop the bot.\n"
        "Use /start to start the bot again.",
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Use /cancel to stop the bot.\n"
        "Use /add_job to add .",
    )

async def add_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """add job the conversation and ask user for input."""
    await update.message.reply_text(
        "مرحبا بك في معالج اضافة الوظائف. "
        "الرجاء اختر نوع الشاغر المطلوب من القائمة",
        reply_markup=markup,
    )

    return CHOOSING

async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(f"Your {text.lower()}? Yes, I would love to hear about that!")
    return TYPING_REPLY


async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text(
        'Alright, please send me the category first, for example "Most impressive skill"')
    return TYPING_CHOICE

async def catagory_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]
    await update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)}You can tell me more, or change your opinion"
        " on something.",
        reply_markup=markup,
    )
    return CHOOSING

async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]
    await update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)}You can tell me more, or change your opinion"
        " on something.",
        reply_markup=markup,
    )
    return CHOOSING

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END


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
                MessageHandler(filters.Regex("^Catagory$"), catagory_choice),
                MessageHandler(filters.Regex("^Something else...$"), custom_choice),],
            TYPING_CHOICE: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), regular_choice)],
            TYPING_REPLY: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),received_information,)],
            },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    application.add_handler(help_handler)
    application.add_handler(start_handler)
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()