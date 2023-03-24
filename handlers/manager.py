from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from main import dp, bot, db
from keyboards.keyboard_manager import cd_request


@dp.callback_query_handler(cd_request.filter(action='answer'))
async def answer(call: CallbackQuery, callback_data: dict):
    lst = dict(await db.check_city(call.from_user.username))
    if callback_data.get('city').lower() in lst["city"].split("-") and callback_data.get('option').lower() in lst["department"].split("-"):
        await bot.send_message(callback_data.get('user_id'),
                               text=f'Контакт менеджера - Ваш личный менеджер @{call.from_user.username}')
        await call.message.delete()
        await call.message.answer(text='Заявка принята')
        await db.update_status(callback_data.get('user_id'), False)
        await db.update_applications(call.from_user.username)
        await db.add_request(callback_data.get('user_id'), callback_data.get('city'), callback_data.get('option'))
    else:
        await call.answer(text=f'Вы не можете принять эту заявку')
