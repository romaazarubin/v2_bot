import os

from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from main import dp, bot, db
from keyboards.keyboard_period import manager_stats_period


@dp.callback_query_handler(text_contains='day_manager')
async def info_manager_day(call: CallbackQuery):
    try:
        year = call.message.date.year
        month = call.message.date.month
        day = call.message.date.day
        data = await db.select_manager_day(year, month, day)
        await call.message.edit_text(text='Статистика по менежерам за день', reply_markup=manager_stats_period(data))
    except:
        await call.message.edit_text(text='Данных нет')


@dp.callback_query_handler(text_contains='month_manager')
async def info_manager_day(call: CallbackQuery):
    try:
        year = call.message.date.year
        month = call.message.date.month
        data = await db.select_manager_month(year, month)
        await call.message.edit_text(text='Статистика по менежерам за месяц', reply_markup=manager_stats_period(data))
    except:
        await call.message.edit_text(text='Данных нет')


@dp.callback_query_handler(text_contains='all_info_manager')
async def info_manager(call: CallbackQuery):
    data = await db.select_applications()
    await call.message.edit_text(text='Статистика по менежерам за все время', reply_markup=manager_stats_period(data))
