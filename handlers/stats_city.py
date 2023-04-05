import os

from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from main import dp, bot, db
from keyboards.keyboard_period import city_stats_period


@dp.callback_query_handler(text_contains='day_city')
async def info_sity(call: CallbackQuery):
    try:
        year = call.message.date.year
        month = call.message.date.month
        day = call.message.date.day
        data = await db.select_city_day(year, month, day)
        await call.message.edit_text(text=f'Статистика по городам за день', reply_markup=city_stats_period(dict(data)))
    except:
        await call.message.edit_text(text='Данных нет')


@dp.callback_query_handler(text_contains='month_city')
async def info_sity(call: CallbackQuery):
    try:
        year = call.message.date.year
        month = call.message.date.month
        data = await db.select_city_month(year, month)
        await call.message.edit_text(text=f'Статистика по городам за месяц', reply_markup=city_stats_period(dict(data)))
    except:
        await call.message.edit_text(text='Данных нет')

@dp.callback_query_handler(text_contains='all_info_city')
async def info_sity(call: CallbackQuery):
    data = await db.count_city()
    await call.message.edit_text(text=f'Статистика по городам', reply_markup=city_stats_period(dict(data)))