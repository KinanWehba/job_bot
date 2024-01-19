from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ContextTypes,ConversationHandler

from dotenv import load_dotenv
import os
import re

from helper_function import facts_to_str
BASE_URL = os.getenv("BASE_URL")
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
    ["خباز"]
]
regex_pattern = f"({'|'.join(map(re.escape, [item[0] for item in reply_keyboard if item[0] != 'Done' if item[0] != 'Something else...'] ))})"
regex_catagory = f"({'|'.join(map(re.escape, [item[0] for item in catagory_list if item[0] != 'Done'] ))})"

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
markup_catagory = ReplyKeyboardMarkup(catagory_list, one_time_keyboard=True)

async def add_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """add job the conversation and ask user for input."""
    await update.message.reply_text(
        "مرحبا بك في معالج اضافة الوظائف. "
        "الرجاء اختر نوع الشاغر المطلوب من القائمة",
        reply_markup=markup,)

    return CHOOSING

async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    if text == 'Catagory' :
        context.user_data["choice"] = text
        msg = ""
        keyboard = []

        for text_list in catagory_list:
            msg = f"{msg}\n{text_list[0]}"
            row = [InlineKeyboardButton(f"{text_list[0]}", callback_data=f"{text_list[0]}")]
            keyboard.append(row)

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:",
        reply_markup=reply_markup,
    )

        return TYPING_REPLY
 
    else :
        context.user_data["choice"] = text
        await update.message.reply_text(f"Your {text.lower()}? Yes, I would love to hear about that!")
        return TYPING_REPLY

async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text(
        'Alright, please send me the category first, for example "Most impressive skill"')
    return TYPING_CHOICE

async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query :
        await query.answer()
        query_data = query.data
        text = query_data
        user_data = context.user_data
        category = user_data["choice"]
        user_data[category] = text
        del user_data["choice"]
        await update.callback_query.message.reply_text(
            "Neat! Just so you know, this is what you already told me:"
            f"{facts_to_str(user_data)}You can tell me more, or change your opinion"
            " on something.",
            reply_markup=markup,)
    else :
        text = update.message.text
        user_data = context.user_data
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
