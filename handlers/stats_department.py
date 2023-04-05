import os

from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from main import dp, bot, db
from keyboards.keyboard_period import department_stats_period

@dp.callback_query_handler(text_contains='day_department')
async def info_applic(call: CallbackQuery):
    try:
        year = call.message.date.year
        month = call.message.date.month
        day = call.message.date.day
        data = await db.select_department_day(year, month, day)
        await call.message.edit_text(text=f'Статистика по услугм за день', reply_markup=department_stats_period(dict(data)))
    except:
        await call.message.edit_text(text='Данных нет')

@dp.callback_query_handler(text_contains='month_department')
async def info_applic(call: CallbackQuery):
    try:
        year = call.message.date.year
        month = call.message.date.month
        data = await db.select_department_month(year, month)
        await call.message.edit_text(text=f'Статистика по услугам за месяц', reply_markup=department_stats_period(dict(data)))
    except:
        await call.message.edit_text(text='Данных нет')

@dp.callback_query_handler(text_contains='all_info_department')
async def info_sity(call: CallbackQuery):
    data = await db.count_department()
    await call.message.edit_text(text=f'Статистика по услугам', reply_markup=department_stats_period(dict(data)))