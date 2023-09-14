from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from main import dp, bot, db
from keyboards.keyboard_manager import cd_request

# Старая версия кода без распределения
# @dp.callback_query_handler(cd_request.filter(action='answer'))
# async def answer(call: CallbackQuery, callback_data: dict):
#     try:
#         lst = dict(await db.check_city(call.from_user.username.lower()))
#         if callback_data.get('city').lower() in lst["city"].split("-") and callback_data.get('option').lower() in lst["department"].split("-"):
#             await bot.send_message(callback_data.get('user_id'),
#                                    text=f'Контакт менеджера - @{call.from_user.username}')
#             username = await db.select_username_client(callback_data.get('user_id'))
#             await call.message.delete()
#             await call.message.answer(text=f'Заявка принята менеджером {call.from_user.username}')
#             await bot.send_message(call.from_user.id, text=f'Контакт клиента - @{username}')
#             await db.manager_app_add(call.from_user.username.lower(), call.message.date.date(), callback_data.get('option').lower(),callback_data.get('city') )
#             await db.update_status(callback_data.get('user_id'), False)
#             await db.update_applications(call.from_user.username)
#             await db.add_request(callback_data.get('user_id'), callback_data.get('city'), callback_data.get('option'))
#         else:
#             await call.answer(text=f'Вы не можете принять эту заявку')
#     except:
#         await call.answer(text='Вы не являетесь менеджером')
