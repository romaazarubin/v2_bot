from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# cd_managerStats = CallbackData('cd_managerStats', 'action', 'username', 'sity')

keyboard_stats = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='По городам', callback_data='infoCity')
        ],
        [
            InlineKeyboardButton(text='По менеджерам', callback_data='infoManager')
        ],
        [
            InlineKeyboardButton(text='По услугам', callback_data='infoApplic')
        ],
        [
            InlineKeyboardButton(text='Вернуться назад', callback_data='admin_main')
        ]

    ]
)


def city_stats(data):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    msk = str(data['s1'])
    irk = str(data['s2'])
    btn1 = InlineKeyboardButton(text=f'Москва: {msk}', callback_data='msk')
    btn2 = InlineKeyboardButton(text=f'Иркутск: {irk}', callback_data='irk')
    btn3 = InlineKeyboardButton(text='Вернуться назад', callback_data='admin_main')
    markup.add(btn1, btn2, btn3)
    return markup

def department_stats(data):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    repair = data["s1"]
    hosting = data["s2"]
    purchase = data["s3"]
    leasing = data["s4"]
    other = data["s5"]
    btn1 = InlineKeyboardButton(text=f'Ремонт: {repair}', callback_data='rep')
    btn2 = InlineKeyboardButton(text=f'Хостинг: {hosting}', callback_data='hos')
    btn3 = InlineKeyboardButton(text=f'Продажа: {purchase}', callback_data='pur')
    btn4 = InlineKeyboardButton(text=f'Лизинг: {leasing}', callback_data='leasing')
    btn5 = InlineKeyboardButton(text=f'Другое:  {other}', callback_data='other')
    btn6 = InlineKeyboardButton(text='Вернуться назад', callback_data='admin_main')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup


def manager_stats(data):
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
