import os

from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from main import dp, bot, db
from keyboards.keyboard_manager import cd_request
from keyboards.keyboard_admin import admin_main, admin_addManager, cd_good_next_menu, cd_good_back_menu, cd_manager, \
    all_manager, client_stats
from config import admin_id
from keyboards.keyboard_stats import keyboard_stats, manager_stats, city_stats, department_stats
from aiogram.dispatcher import FSMContext
from state.add_state import AddManager


@dp.callback_query_handler(cd_request.filter(action='cancel'))
async def cancel_request(call: CallbackQuery, callback_data: dict):
    if call.from_user.id in admin_id:
        await call.message.delete()
        await db.update_status(callback_data.get('user_id'), False)
        await call.answer(text="Заявка удалена")
    else:
        await call.answer(text="У вас не хватает прав")


@dp.message_handler(Command('admin'))
async def admin_main_menu(message: Message):
    if message.from_user.id in admin_id:
        await bot.send_message(chat_id=message.from_user.id, text='Основное меню - УПРАВЛЕНИЕ', reply_markup=admin_main)


@dp.callback_query_handler(text_contains='edit_list_manager')
async def edit_list_manager(call: CallbackQuery):
    await call.message.edit_text(text='Редактирование списка менеджеров', reply_markup=admin_addManager)


@dp.callback_query_handler(text_contains='admin_main')
async def admin_back_main(call: CallbackQuery):
    await call.message.edit_text(text='Основное меню - УПРАВЛЕНИЕ ', reply_markup=admin_main)


@dp.callback_query_handler(text_contains='add_manager')
async def add_manager(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text='Введите username менеджера')
    await AddManager.username.set()


@dp.message_handler(state=AddManager.username)
async def username(message: Message, state: FSMContext):
    await state.update_data(
        {
            'username': str(message.text)
        }
    )
    await bot.send_message(message.from_user.id,
                           text='Введите город, если он не один то вводите через "-". Пример "Москва-Иркутск"')
    await AddManager.city.set()


@dp.message_handler(state=AddManager.city)
async def username(message: Message, state: FSMContext):
    await state.update_data(
        {
            'city': str(message.text)
        }
    )
    await bot.send_message(message.from_user.id,
                           text='Введите услугу, если онa не однa то вводите через "-". Пример "Ремонт-Хостинг-Покупка-Другое"')
    await AddManager.department.set()


@dp.message_handler(state=AddManager.department)
async def username(message: Message, state: FSMContext):
    data = await state.get_data()
    k = await db.presence_manager(data.get("username"))
    if not k:
        await db.add_manager(data.get("username").lower(), data.get("city").lower(), message.text.lower())
        await bot.send_message(message.from_user.id,
                               text=f'Username:{data.get("username")}\n'
                                    f'Город:{data.get("city")}\n'
                                    f'Услуги:{message.text}\n'
                                    f'Добавлен в менеджеры!',
                               reply_markup=admin_main)
    else:
        await bot.send_message(message.from_user.id,
                               text=f'Username:{data.get("username")}\n'
                                    f'Город:{data.get("city")}\n'
                                    f'Услуги:{message.text}\n'
                                    f'Уже есть в списке!',
                               reply_markup=admin_main)
    await state.finish()


@dp.callback_query_handler(cd_good_next_menu.filter(action='next', type='manager'))
async def next_menu(call: CallbackQuery, callback_data: dict):
    call_info = call.data.split(":")[0] + call.data.split(":")[3]
    data = await db.all_manager(int(callback_data.get('step')))
    count = await db.count_manager()
    await call.message.edit_reply_markup(
        reply_markup=all_manager(data, count, call_info, int(callback_data.get('step'))))


@dp.callback_query_handler(cd_good_back_menu.filter(action='backwards', type='manager'))
async def back_menu(call: CallbackQuery, callback_data: dict):
    call_info = call.data.split(":")[0] + call.data.split(":")[3]
    data = await db.all_manager(int(callback_data.get('step')))
    count = await db.count_manager()
    await call.message.edit_reply_markup(
        reply_markup=all_manager(data, count, call_info, int(callback_data.get('step'))))


@dp.callback_query_handler(cd_manager.filter(action='delete'))
async def delete_manag(call: CallbackQuery, callback_data: dict):
    try:
        await db.delete_manager(callback_data.get('username'), callback_data.get('city'))
        data = await db.all_manager(0)
        count = await db.count_manager()
        await call.message.edit_reply_markup(reply_markup=all_manager(data, count, call.data.split(":")[0]))
    except:
        await call.answer('Произошла ошибка')
        await call.message.edit_text(text='Основное меню - УПРАВЛЕНИЕ', reply_markup=admin_main)


@dp.callback_query_handler(text_contains='remove_manager')
async def remove_manager(call: CallbackQuery):
    data = await db.all_manager(0)
    count = await db.count_manager()
    await call.message.edit_text(text='Список менеджеров, для удаление нажмините',
                                 reply_markup=all_manager(data, count, call.data))


@dp.callback_query_handler(text_contains='stats')
async def stats(call: CallbackQuery):
    await call.message.edit_text(text='Получить информацию по ...', reply_markup=keyboard_stats)


@dp.callback_query_handler(text_contains='infoManager')
async def info_manager(call: CallbackQuery):
    data = await db.select_applications()
    await call.message.edit_text(text='Статистика по менежерам', reply_markup=manager_stats(data))


@dp.callback_query_handler(text_contains='list_client_txt')
async def list_client_txt(call: CallbackQuery):
    try:
        await call.message.delete()
        data = await db.all_client_txt()
        with open("infoClient.txt", "w") as file:
            for i in data:
                file.write(f"{str(i['username'])}\n")
        await bot.send_document(call.from_user.id, document=open("infoClient.txt", "rb"))
        await call.message.answer(text='Основное меню - УПРАВЛЕНИЕ',  reply_markup=admin_main)
        os.remove("infoClient.txt")
    except:
        os.remove("infoClient.txt")
        await call.message.answer(text='В списке нет клиентов', reply_markup=admin_main)

@dp.callback_query_handler(text_contains='list_client_menu')
async def list_client_menu(call: CallbackQuery):
    data = await db.all_client(0)
    count = await db.count_client()
    await call.message.edit_text(text='Список клиентов', reply_markup=all_manager(data, count, call.data))

@dp.callback_query_handler(text_contains='list_client')
async def list_client(call: CallbackQuery):
    await call.message.edit_text(text='Получить информацию в ...', reply_markup=client_stats)


@dp.callback_query_handler(cd_good_next_menu.filter(action='next', type='client'))
async def next_menu(call: CallbackQuery, callback_data: dict):
    call_info = call.data.split(":")[0] + call.data.split(":")[3]
    data = await db.all_client(int(callback_data.get('step')))
    count = await db.count_client()
    await call.message.edit_reply_markup(
        reply_markup=all_manager(data, count, call_info, int(callback_data.get('step'))))


@dp.callback_query_handler(cd_good_back_menu.filter(action='backwards', type='client'))
async def back_menu(call: CallbackQuery, callback_data: dict):
    call_info = call.data.split(":")[0] + call.data.split(":")[3]
    data = await db.all_client(int(callback_data.get('step')))
    count = await db.count_client()
    await call.message.edit_reply_markup(
        reply_markup=all_manager(data, count, call_info, int(callback_data.get('step'))))


@dp.callback_query_handler(text_contains='infoCity')
async def info_sity(call: CallbackQuery):
    data = await db.count_city()
    await call.message.edit_text(text=f'Статистика по городам', reply_markup=city_stats(dict(data)))

@dp.callback_query_handler(text_contains='infoApplic')
async def info_applic(call: CallbackQuery):
    data = await db.count_department()
    await call.message.edit_text(text=f'Статистика по услугам', reply_markup=department_stats(dict(data)))
