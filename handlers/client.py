from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from main import dp, bot, db
from keyboards.keyboard_client import button_city, button_option, keyboard_city, cd_option
from keyboards.keyboard_manager import cd_request, keyboard_request
from config import chat_id


@dp.message_handler(Command('start'))
async def start(message: Message):
    try:
        k = await db.presence_user(message.from_user.id)
        if not k:
            await db.add_user(message.from_user.id, message.from_user.username)
    except:
        pass
    try:
        # status = await db.check_status(message.from_user.id)
        # if status:
        # await bot.send_message(message.from_user.id,
        #                      text='Вы уже отправили запрос, подождите пока вам на него ответят')
        # else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Выберите услугу:',
                               reply_markup=button_option)
    except:
        await bot.send_message(message.from_user.id,
                               text='Произошла ошибка попробуйте позже')


# @dp.message_handler(Command('menu'))
# async def option(message: Message):
#     try:
#         k = await db.presence_user(message.from_user.id)
#         if not k:
#             await db.add_user(message.from_user.id, message.from_user.username)
#     except:
#         pass
#     try:
#         status = await db.check_status(message.from_user.id)
#         if status:
#             await bot.send_message(message.from_user.id,
#                                    text='Вы уже отправили запрос, подождите пока вам на него ответят')
#         else:
#             await bot.send_message(chat_id=message.from_user.id,
#                                    text='Выберите услугу',
#                                    reply_markup=button_option)
#     except:
#         await bot.send_message(message.from_user.id,
#                                text='Произошла ошибка попробуйте позже')


@dp.callback_query_handler(Text(equals=['ремонт', 'хостинг', 'покупка', 'другое']))
async def city(call: CallbackQuery):
    await call.message.edit_text(text='Выберите город', reply_markup=keyboard_city(call.data, call.from_user.id))


# Старая версия кода без распределения
# @dp.callback_query_handler(cd_option.filter(action='request')) # async def cd(call: CallbackQuery, callback_data: dict):
#     try:
#         await db.update_status(call.from_user.id, True)
#     except:
#         pass
#     finally:
#         await call.message.edit_text(text='Запрос отправлен')
#         await bot.send_message(chat_id,
#                                text=f'Пользователь {call.from_user.username} из города {callback_data.get("city")} оставил завку на {callback_data.get("option")}',
#                                reply_markup=keyboard_request(callback_data.get("option"),
#                                                              callback_data.get("user_id"),
#                                                              callback_data.get("city")))

# Новая версия кода распределения
@dp.callback_query_handler(cd_option.filter(action='request'))
async def cd(call: CallbackQuery, callback_data: dict):
    manager = await db.select_manager(callback_data.get("city").lower(), callback_data.get("option"))
    if manager is None:
        await call.message.edit_text(text=f'На данный момент нет свободных менеджеров по вашему вопросу')
    else:
        await db.update_manager(manager['manager_id'])
        await call.message.edit_text(text=f'Ваш менеджер - {"@" + str(manager["username"])}')
        await bot.send_message(manager['manager_id'], text=f'Контакт клиента - @{call.from_user.username}')
        await db.add_request(callback_data.get('user_id'), callback_data.get('city'), callback_data.get('option'))
        await db.manager_app_add(str(manager["username"]).lower(), call.message.date.date(),
                                 callback_data.get('option').lower(), callback_data.get('city'))
        # await db.del_manager(manager['manager_id'])
        # await db.comeback_manager(manager['username'], manager['city'], manager['department'], manager['applications'],
        #                           manager['manager_id'])
        # await db.update_applications(manager['username'])


@dp.callback_query_handler(text_contains='back_main_menu')
async def back(call: CallbackQuery):
    try:
        status = await db.check_status(call.from_user.id)
        if status:
            await bot.call.message.edit_text(text='Вы уже отправили запрос, подождите пока вам на него ответят')
        else:
            await call.message.edit_text(text='Выберите услугу',
                                         reply_markup=button_option)
    except:
        await call.message.edit_text(text='Произошла ошибка попробуйте позже')


@dp.callback_query_handler(text_contains='city_cancel')
async def city_cancel(call: CallbackQuery):
    await call.message.edit_text(text='Чем я могу вам помочь ?Выбрать услугу - /start')
