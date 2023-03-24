from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

cd_option = CallbackData('cd_option', 'action', 'option', 'user_id', 'city')



def keyboard_city(option, user_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    btn_moscow = InlineKeyboardButton(text='Москва',
                                      callback_data=cd_option.new(action='request',
                                                                  option=option,
                                                                  user_id=user_id,
                                                                  city='Москва'))

    btn_irkutsk = InlineKeyboardButton(text='Иркутск',
                                       callback_data=cd_option.new(action='request',
                                                                   option=option,
                                                                   user_id=user_id,
                                                                   city='Иркутск'))

    btn_back = InlineKeyboardButton(text='Назад', callback_data='back_main_menu')

    btn_cancel = InlineKeyboardButton(text='Отмена', callback_data='city_cancel')
    markup.add(btn_moscow, btn_irkutsk)
    markup.add(btn_back,btn_cancel)
    return markup

button_city = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Москва', callback_data='Moskva')
        ],
        [
            InlineKeyboardButton(text='Иркутск', callback_data='Irkutsk')
        ]
    ]
)

button_option = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Покупка оборудования', callback_data='покупка')
        ],
        [
            InlineKeyboardButton(text='Хостинг', callback_data='хостинг')
        ],
        [
            InlineKeyboardButton(text='Ремонт оборудования', callback_data='ремонт')
        ],
        [
            InlineKeyboardButton(text='Лизинг', callback_data='лизинг')
        ],
        [
            InlineKeyboardButton(text='Другой вопрос', callback_data='другое')
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='city_cancel')
        ]
    ]
)
