from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.callback_data import CallbackData

cd_manager = CallbackData('cd_manager', 'action', 'username', 'city')
cd_good_next_menu = CallbackData('next', 'action', 'step', 'type')
cd_good_back_menu = CallbackData('back', 'action', 'step', 'type')

admin_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Редактирование списка менеджеров', callback_data='edit_list_manager')
        ],
        [
            InlineKeyboardButton(text='Статистика', callback_data='stats')
        ],
        [
            InlineKeyboardButton(text='Клиенты', callback_data='list_client')
        ]
    ]
)

admin_addManager = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить менеджера', callback_data='add_manager')
        ],
        [
            InlineKeyboardButton(text='Удалить менеджера', callback_data='remove_manager')
        ],
        [
            InlineKeyboardButton(text='Вернуться назад', callback_data='admin_main')
        ]
    ]
)


def all_manager(data, count, call, step=0):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    k = step

    if call == 'remove_manager' or call == 'nextmanager' or call == 'backmanager' or call == 'cd_manager':
        for i in data:
            username = i['username']
            city = i['city']
            btn_product = InlineKeyboardButton(text=f'Менеджер: {username}, город: {city}',
                                               callback_data=cd_manager.new(action='delete',
                                                                            username=username,
                                                                            city=city))
            markup.add(btn_product)
        btn_back_search_sellers = InlineKeyboardButton(text='Назад', callback_data='admin_main')
        markup.add(btn_back_search_sellers)
        next = InlineKeyboardButton(text='>>>', callback_data=cd_good_next_menu.new(action='next',
                                                                                    step=k + 5,
                                                                                    type='manager'))
        back = InlineKeyboardButton(text='<<<', callback_data=cd_good_back_menu.new(action='backwards',
                                                                                    step=k - 5,
                                                                                    type='manager'))
        if k < 5:
            markup.add(next)
        elif count <= k:
            markup.add(back)
        else:
            markup.row(back, next)
        return markup

    elif call == 'list_client' or call == 'nextclient' or call == 'backclient':
        for i in data:
            username = i['username']
            if username == None:
                btn_client = InlineKeyboardButton(text=f'Покупатель: None',
                                                  callback_data='None')
            else:
                btn_client = InlineKeyboardButton(text=f'Покупатель: {username}',
                                                  callback_data=username)
            markup.add(btn_client)
        btn_back_search_sellers = InlineKeyboardButton(text='Назад', callback_data='admin_main')
        markup.add(btn_back_search_sellers)
        next = InlineKeyboardButton(text='>>>', callback_data=cd_good_next_menu.new(action='next',
                                                                                    step=k + 5,
                                                                                    type='client'))
        back = InlineKeyboardButton(text='<<<', callback_data=cd_good_back_menu.new(action='backwards',
                                                                                    step=k - 5,
                                                                                    type='client'))
        if k < 5:
            markup.add(next)
        elif count <= k:
            markup.add(back)
        else:
            markup.row(back, next)
        return markup
