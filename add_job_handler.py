from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ContextTypes,ConversationHandler

import os
import re

from helper_function import base_request

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
reply_keyboard = [
    ["عنوان العمل"],
    ["تفصيل العمل"],
    ["اسم المؤسسة"],
    # ["اضافة تفصيل"],
    ["حفظ"],
]
category_list = ["طبيب","استاذ","خباز"]
regex_pattern = f"({'|'.join(map(re.escape, [item[0] for item in reply_keyboard if item[0] != 'حفظ'
                                            #   if item[0] != "اضافة تفصيل"
                                              ] ))})"
regex_category = f"({'|'.join(map(re.escape, [item for item in category_list] ))})"
input_field_placeholder = "الرجاء الاختيار من القائمة"
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,input_field_placeholder = input_field_placeholder)


async def add_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """add job the conversation and ask user for input."""
    context.user_data["choice"] = 'المسمى الوظيفي'
    msg = ""
    keyboard = []

    for text_list in category_list:
        msg = f"{msg}\n{text_list}"
        row = [InlineKeyboardButton(f"{text_list}", callback_data=f"{text_list}")]
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
    "مرحبا بك في معالج اضافة الوظائف. الرجاء اختر نوع الشاغر (التنصيف ) المطلوب من القائمة\n"
    # "او يمكنك كتابته في حال لم يكن موجود في القائمة"
    ""
    ,
    reply_markup=reply_markup,)

    return TYPING_REPLY

async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(f"اكتب {text.lower()}\n\n.",)
    return TYPING_REPLY

# async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Ask the user for a description of a custom category."""
#     await update.message.reply_text(
#         'ادخل اسم الحقل فقط مثال "الراتب"\n\n.',)
#     return TYPING_CHOICE

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
            f"تم اضافة {category} بنجاح\n"
            # "يمكنك اضافة حقول غير موجودة باستخدام زر اضافة تفصيل\n\n."
            ,
            reply_markup=markup,)
    else :
        text = update.message.text
        user_data = context.user_data
        category = user_data["choice"]
        user_data[category] = text
        del user_data["choice"]
        await update.message.reply_text(
            f"تم اضافة {category} بنجاح\n"
            # "يمكنك اضافة حقول غير موجودة باستخدام زر اضافة تفصيل\n\n."
            ,
            reply_markup=markup,
        )
    return CHOOSING


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
            f"تم اضافة {category} بنجاح\n"
            # "يمكنك اضافة حقول غير موجودة باستخدام زر اضافة تفصيل\n\n."
            ,
            reply_markup=markup,)
    else :
        text = update.message.text
        user_data = context.user_data
        category = user_data["choice"]
        user_data[category] = text
        del user_data["choice"]
        await update.message.reply_text(
            f"تم اضافة {category} بنجاح\n"
            # "يمكنك اضافة حقول غير موجودة باستخدام زر اضافة تفصيل\n\n."
            ,
            reply_markup=markup,
        )
    return CHOOSING

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]
    user_data["chat_id"] = update.message.from_user.id
    print(user_data)
    req = base_request(user_data,'add_job','json')
    await update.message.reply_text(
        f"سيظهر اعلانك كالتالي : {req}",
        reply_markup=ReplyKeyboardRemove(),)

    user_data.clear()
    return ConversationHandler.END
