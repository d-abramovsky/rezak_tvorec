from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery

from config import superuser
from database import Database
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from inline_keyboard import mailing_key, confirm_mailing_key
from datetime import datetime
import pygsheets
from aiogram.utils.markdown import hlink


path = 'service_account_spreadsheets.json'
gc = pygsheets.authorize(service_account_file=path)
sh = gc.open('Rezak Tvorec')
wk = sh[0]


db = Database('db.db')
mail = Router()

class new_mail(StatesGroup):
    get_name = State()
    start_mail = State()
    buttons_mail = State()
    finish_mail = State()
    watch = State()

@mail.message(Command('mailing'))
async def start_mailing(message: Message, state: FSMContext):
    if (int(message.from_user.id) == superuser and list(*db.get_lang(message.from_user.id))[0] == 'RU') or \
            (str(message.from_user.id) in [str(db.get_admin_id_mail()[x][0]) for x in range(len(db.get_admin_id_mail()))] and list(*db.get_lang(message.from_user.id))[0] == 'RU'):
        await message.answer(text = 'Как называется рассылка?')
        await state.set_state(new_mail.get_name)

@mail.message(Command('watchmailing'))
async def start_mailing(message: Message, bot: Bot, state: FSMContext):
    if (int(message.from_user.id) == superuser and list(*db.get_lang(message.from_user.id))[0] == 'RU') or \
            (str(message.from_user.id) in [str(db.get_admin_id_mail()[x][0]) for x in range(len(db.get_admin_id_mail()))] and list(*db.get_lang(message.from_user.id))[0] == 'RU'):
        await message.answer(text = 'Введите номер строки в которой находится интересующая вас рассылка.')
        await state.set_state(new_mail.watch)

@mail.message(new_mail.watch)
async def start_mailing(message: Message, bot: Bot, state: FSMContext):
    await message.answer(text = 'Отправляю рассылку!')
    message_id = wk.get_row(row = int(message.text), include_tailing_empty = False)[1]
    name, user_id, buttons = list(*db.get_mailing(message_id))
    buttons = buttons.split('\n') if buttons != None else None
    if buttons != None:
        builder = InlineKeyboardBuilder()
        for x in range(int(len(buttons)/2)):
            builder.button(text=buttons[0], url=buttons[1])
    else:
        builder = InlineKeyboardBuilder()
    await bot.copy_message(chat_id=message.from_user.id, message_id=int(message_id), from_chat_id=user_id, reply_markup=builder.as_markup())
    await state.clear()

@mail.message(new_mail.get_name)
async def start_mailing(message: Message, state: FSMContext):
    await message.answer(text = 'Отправьте рекламное сообщение')
    await state.update_data(name = message.text)
    await state.set_state(new_mail.start_mail)

@mail.message(new_mail.start_mail)
async def mailing_message(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(message_id=f'{message.message_id}')
    await state.update_data(from_chat_id=f'{message.from_user.id}')
    await message.answer(text = 'Принято, запомнил это сообщение! Будут ли рекламные кнопки?', reply_markup=mailing_key)
    await state.set_state(new_mail.buttons_mail)

@mail.callback_query(new_mail.buttons_mail, F.data == "mail_1")
async def mailing_buttons(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.answer()
    await bot.send_message(chat_id=call.from_user.id, text='Отправьте ссылку и текст для кнопок. Пример:\n'
                                                           'Текст кнопки\n'
                                                           'Ссылка для этой кнопки\n'
                                                           '(К сообщению можно прикрепить несколько кнопок)')
    await state.set_state(new_mail.finish_mail)



@mail.callback_query(new_mail.buttons_mail, F.data == "mail_0")
async def mailing_finish_no_buttons(call: CallbackQuery, state: FSMContext, bot: Bot):
    context_data = await state.get_data()
    await call.answer()
    message_id = int(context_data.get('message_id'))
    from_chat_id = int(context_data.get('from_chat_id'))
    await bot.copy_message(chat_id=call.from_user.id, message_id=message_id, from_chat_id=from_chat_id)
    await bot.send_message(chat_id=call.from_user.id, text='Рекламное сообщение сформировано!\n'
                                                           'Будем отправлять?', reply_markup=confirm_mailing_key)
@mail.message(new_mail.finish_mail)
async def mailing_finish(message: Message, state: FSMContext, bot: Bot):
    context_data = await state.get_data()
    message_id = int(context_data.get('message_id'))
    from_chat_id = int(context_data.get('from_chat_id'))
    buttons = message.text.split('\n')
    await state.update_data(buttons=message.text)
    builder = InlineKeyboardBuilder()
    if len(buttons)%2==0:
        for x in range(int(len(buttons)/2)):
            builder.button(text=buttons[0], url=buttons[1])
        await bot.copy_message(chat_id=message.from_user.id, message_id=message_id, from_chat_id=from_chat_id,
                               reply_markup=builder.as_markup())
        await bot.send_message(chat_id=message.from_user.id, text='Рекламное сообщение сформировано!\n'
                                                                  'Будем отправлять?', reply_markup=confirm_mailing_key)

    else:
        await message.answer('Недостаточно данных, отправьте информацию для кнопок заново. Пример:\n'
                                                           'Текст кнопки\n'
                                                           'Ссылка для этой кнопки\n'
                                                           '(К сообщению можно прикрепить несколько кнопок)')
        await state.set_state(new_mail.finish_mail)

@mail.callback_query(F.data == "confirm_mail")
async def mailing_sender(call: CallbackQuery, state: FSMContext, bot: Bot):
    if (int(call.from_user.id) == superuser and list(*db.get_lang(call.from_user.id))[0] == 'RU') or \
            (str(call.from_user.id) in [str(db.get_admin_id_mail()[x][0]) for x in range(len(db.get_admin_id_mail()))] and list(*db.get_lang(call.from_user.id))[0] == 'RU'):
        await bot.send_message(chat_id=call.from_user.id, text = 'Начал рассылку! Оповещу вас, когда закончу.')
        context_data = await state.get_data()
        await call.answer()
        message_id = int(context_data.get('message_id'))
        name = context_data.get('name')
        from_chat_id = int(context_data.get('from_chat_id'))
        buttons = context_data.get('buttons').split('\n') if context_data.get('buttons') != None else None
        button =context_data.get('buttons') if context_data.get('buttons') != None else None
        db.add_mailing(name, message_id, from_chat_id, button)
        db.commit()
        users = db.get_all_users()
        user_tup = [users[x][0] for x in range(len(users))]
        if buttons != None:
            builder = InlineKeyboardBuilder()
            for x in range(int(len(buttons) / 2)):
                builder.button(text=buttons[0], url=buttons[1])
        else:
            builder = InlineKeyboardBuilder()
        for user in user_tup:
            try:
                await bot.copy_message(chat_id=int(user), message_id=message_id, from_chat_id=from_chat_id, reply_markup=builder.as_markup())
            except:
                db.user_set_active('0', user)
        await bot.send_message(chat_id=call.from_user.id, text = f'Рассылка закончена!\n'
                                                                 f'Сообщение отправлено {len(db.get_all_users())} пользователям')
        send_users = str(len(db.get_all_users()))
        all_users = str(db.get_count_users()[0])
        date = str(datetime.today())[:-7]
        percent = float((int(all_users)/int(send_users))/100)
        wk.insert_rows(row = 1, number = 1, values = [name, message_id, send_users, all_users, percent, date])
        table = hlink('таблицу',
                     'https://docs.google.com/spreadsheets/d/15e-eJbkJtFDQF0ogdictlK7vHmmUfuK6iiuNJ-DTFs0/edit?gid=0#gid=0')
        await bot.send_message(chat_id=call.from_user.id, text = f'Подгрузил данные о расслылке в {table}.\n'
                                                                 f'Не хотите посмотреть?', disable_web_page_preview=True)
        await state.clear()
    await call.answer()



