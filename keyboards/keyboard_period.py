from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# менеджеры
keyboard_period_manager = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='За день', callback_data='day_manager')
        ],
        [
            InlineKeyboardButton(text='За месяц', callback_data='month_manager')
        ],
        [
            InlineKeyboardButton(text='За все время', callback_data='all_info_manager')
        ],
        [
            InlineKeyboardButton(text='Вернуться назад', callback_data='admin_main')
        ]

    ]
)


def manager_stats_period(data):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for i in data:
        username = i['username']
        applications = i['applications']
        btn_product = InlineKeyboardButton(text=f'Менеджер: {username}, кол-во: {applications}',
                                           callback_data=username)
        markup.add(btn_product)
    btn_back_search_sellers = InlineKeyboardButton(text='Назад', callback_data='admin_main')
    markup.add(btn_back_search_sellers)
    return markup


# города
keyboard_period_city = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='За день', callback_data='day_city')
        ],
        [
            InlineKeyboardButton(text='За месяц', callback_data='month_city')
        ],
        [
            InlineKeyboardButton(text='За все время', callback_data='all_info_city')
        ],
        [
            InlineKeyboardButton(text='Вернуться назад', callback_data='admin_main')
        ]

    ]
)


def city_stats_period(data):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    msk = str(data['s1'])
    irk = str(data['s2'])
    btn1 = InlineKeyboardButton(text=f'Москва: {msk}', callback_data='msk')
    btn2 = InlineKeyboardButton(text=f'Иркутск: {irk}', callback_data='irk')
    btn3 = InlineKeyboardButton(text='Вернуться назад', callback_data='admin_main')
    markup.add(btn1, btn2, btn3)
    return markup


# услуги
keyboard_period_department = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='За день', callback_data='day_department')
        ],
        [
            InlineKeyboardButton(text='За месяц', callback_data='month_department')
        ],
        [
            InlineKeyboardButton(text='За все время', callback_data='all_info_department')
        ],
        [
            InlineKeyboardButton(text='Вернуться назад', callback_data='admin_main')
        ]

    ]
)
def department_stats_period(data):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    repair = data["s1"]
    hosting = data["s2"]
    purchase = data["s3"]
    other = data["s4"]
    btn1 = InlineKeyboardButton(text=f'Ремонт: {repair}', callback_data='rep')
    btn2 = InlineKeyboardButton(text=f'Хостинг: {hosting}', callback_data='hos')
    btn3 = InlineKeyboardButton(text=f'Продажа: {purchase}', callback_data='pur')
    btn4 = InlineKeyboardButton(text=f'Другое:  {other}', callback_data='other')
    btn5 = InlineKeyboardButton(text='Вернуться назад', callback_data='admin_main')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup

