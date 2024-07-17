from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hlink
from database import Database
from config import superuser
from aiogram.utils.keyboard import InlineKeyboardBuilder
from inline_keyboard import admin_keyboard_change_level, admin_change_level_key
from aiogram.filters.command import Command, CommandObject

db = Database('db.db')
adm = Router()


@adm.message(Command('admins'))
async def start_admins(message: Message):
    if message.from_user.id == superuser:
        admins_list = db.get_admins()
        admins = f''
        for x in range(len(admins_list)):
            admin_id, menu, gallery, mailing, statistics = admins_list[x]
            menu_text = 'Меню и карточки товара\n' if int(menu) == 1 else ''
            gallery_text = 'Галерея\n' if int(gallery) == 1 else ''
            mailing_text = 'Рассылка\n' if int(mailing) == 1 else ''
            statistics_text = 'Статистика' if int(statistics) == 1 else ''
            try:
                web = f'https://t.me/{list(*db.get_username(admin_id))[0]}'
                if menu + gallery + mailing + statistics != '0000':
                    admins += (f'{hlink(list(*db.get_username(admin_id))[0], web)}:\n'
                               f'{menu_text} {gallery_text} {mailing_text} {statistics_text}\n')
                else:
                    admins += (f'{hlink(list(*db.get_username(admin_id))[0], web)}:\n'
                               f'Права отсутствуют\n')
            except IndexError:
                pass
        await message.answer(text=f'Вот список администраторов:\n'
                                  f'{admins}', disable_web_page_preview=True, reply_markup=admin_keyboard_change_level)

@adm.message(Command('new_admin'))
async def add_admins(message: Message, command: CommandObject):
    await message.answer(text=f'Новый админ {list(*db.get_username(command.args))[0]} добавлен!')
    db.add_admin(message.from_user.id)
    db.commit()

@adm.message(Command('delete_admin'))
async def add_admins(message: Message, command: CommandObject):
    await message.answer(text=f'Админ {list(*db.get_username(command.args))[0]} удален!')
    db.delete_admin(message.from_user.id)
    db.commit()

@adm.callback_query(F.data == "change_admin_level")
async def mailing_buttons(call: CallbackQuery, bot: Bot):
    builder = InlineKeyboardBuilder()
    admins_list = db.get_admins()
    for x in range(len(admins_list)):
        admin_id = admins_list[x][0]
        builder.button(text=f'{list(*db.get_username(admin_id))[0]}', callback_data=f'admin:{admin_id}')
    builder.adjust(2)
    await bot.send_message(chat_id=call.from_user.id, text='Кому будем изменять права?', reply_markup=builder.as_markup())
    await call.message.delete()
    await call.answer()


@adm.callback_query(F.data.startswith('admin:'))
async def mailing_buttons(call: CallbackQuery, bot: Bot):
    admin_id = call.data[6:]
    admin_id, menu, gallery, mailing, statistics = list(*db.get_admin(admin_id))
    await call.message.delete()
    web = f'https://t.me/{list(*db.get_username(admin_id))[0]}'
    await bot.send_message(chat_id=call.from_user.id, text=f'Какие права будут у администратора {hlink(list(*db.get_username(admin_id))[0], web)}', reply_markup=admin_change_level_key(admin_id, menu, gallery, mailing, statistics))
    await call.answer()

@adm.callback_query(F.data.startswith('adm:'))
async def mailing_buttons(call: CallbackQuery, bot: Bot):
    data = call.data[4:8]
    if data != 'stop':
        admin_id = call.data[9:]
        admin_id, menu, gallery, mailing, statistics = list(*db.get_admin(admin_id))
        if data == 'card':
            num = '1' if menu == '0' else '0'
            db.update_admin_change_menu(num, admin_id)
        elif data == 'gall':
            num = '1' if gallery == '0' else '0'
            db.update_admin_change_gallery(num, admin_id)
        elif data == 'mail':
            num = '1' if mailing == '0' else '0'
            db.update_admin_mailing(num, admin_id)
        elif data == 'stat':
            num = '1' if statistics == '0' else '0'
            db.update_admin_get_statistics(num, admin_id)
        admin_id, menu, gallery, mailing, statistics = list(*db.get_admin(admin_id))
        web = f'https://t.me/{list(*db.get_username(admin_id))[0]}'
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=f'Какие права будут у администратора {hlink(list(*db.get_username(admin_id))[0], web)}', reply_markup=admin_change_level_key(admin_id, menu, gallery, mailing, statistics))
    else:
        admins_list = db.get_admins()
        admins = f''
        for x in range(len(admins_list)):
            admin_id, menu, gallery, mailing, statistics = admins_list[x]
            menu_text = 'Меню и карточки товара\n' if int(menu) == 1 else ''
            gallery_text = 'Галерея\n' if int(gallery) == 1 else ''
            mailing_text = 'Рассылка\n' if int(mailing) == 1 else ''
            statistics_text = 'Статистика\n' if int(statistics) == 1 else ''
            try:
                web = f'https://t.me/{list(*db.get_username(admin_id))[0]}'
                if menu + gallery + mailing + statistics != '0000':
                    admins += (f'{hlink(list(*db.get_username(admin_id))[0], web)}:\n'
                               f'{menu_text} {gallery_text} {mailing_text} {statistics_text}\n')
                else:
                    admins += (f'{hlink(list(*db.get_username(admin_id))[0], web)}:\n'
                               f'Права отсутствуют\n')
            except IndexError:
                pass
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=f'Вот список администраторов:\n'
                                  f'{admins}', disable_web_page_preview=True, reply_markup=admin_keyboard_change_level)

    db.commit()
    await call.answer()
