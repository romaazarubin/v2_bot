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
    finally:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Приветствую! Я бот компании Leomining, готов помочь вам с любыми вопросами, '
                                    'связанными с оборудованием для майнинга криптовалют. Чем я могу вам помочь ? '
                                    'Выбрать услугу - /menu')


@dp.message_handler(Command('menu'))
async def option(message: Message):
    try:
        status = await db.check_status(message.from_user.id)
        if status:
            await bot.send_message(message.from_user.id,
                                   text='Вы уже отправили запрос, подождите пока вам на него ответят')
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Выберите услугу',
                                   reply_markup=button_option)
    except:
        await bot.send_message(message.from_user.id,
                               text='Произошла ошибка попробуйте позже')


@dp.callback_query_handler(Text(equals=['ремонт', 'хостинг', 'покупка', 'лизинг', 'другое']))
async def city(call: CallbackQuery):
    await call.message.edit_text(text='Выберите город', reply_markup=keyboard_city(call.data, call.from_user.id))


@dp.callback_query_handler(cd_option.filter(action='request'))
async def cd(call: CallbackQuery, callback_data: dict):
    try:
        await db.update_status(call.from_user.id, True)
    except:
        pass
    finally:
        await call.message.edit_text(text='Запрос отправлен')
        await bot.send_message(chat_id,
                               text=f'Пользователь {call.from_user.username} из города {callback_data.get("city")} оставил завку на {callback_data.get("option")}',
                               reply_markup=keyboard_request(callback_data.get("option"),
                                                             callback_data.get("user_id"),
                                                             callback_data.get("city")))


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
    await call.message.edit_text(text='Чем я могу вам помочь ?Выбрать услугу - /menu')