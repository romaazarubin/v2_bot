from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

cd_request = CallbackData('cd_request', 'action', 'option', 'user_id', 'city')

def keyboard_request(option, user_id, city):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    btn_answer = InlineKeyboardButton(text='Принять',
                                      callback_data=cd_request.new(action='answer',
                                                                   option=option,
                                                                   user_id=user_id,
                                                                   city=city))
    button_cancel = InlineKeyboardButton(text='Удалить обращение',
                                         callback_data=cd_request.new(action='cancel',
                                                                      option=option,
                                                                      user_id=user_id,
                                                                      city=city))
    markup.add(btn_answer, button_cancel)
    return markup
