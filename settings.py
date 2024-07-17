from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, PollAnswer
from aiogram.filters.command import Command
from database import Database
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext
from inline_keyboard import settings, deactivate, deactivate_eng
from reply_keyboard import phone, keyboard, keyboard_eng

sett = Router()
db = Database('db.db')

class settings_user(StatesGroup):
    settings_name = State()
    settings_age = State()
    settings_number = State()
    settings_email = State()
    settings_lang = State()


@sett.message(Command('settings'))
async def setting(message: Message, bot: Bot):
    lang = list(*db.get_lang(message.from_user.id))[0]
    info = [x if x != None else 'Отсутствует' for x in list(*db.get_user(message.from_user.id))]
    info_eng = [x if x != None else 'Not found' for x in list(*db.get_user(message.from_user.id))]
    text = (f'Вы перешли в раздел "Настройки".\n'
            f'Здесь вы можете заполнить данные о себе.\n'
            f'*ID:* `{message.from_user.id}`\n'
            f'*Имя:* {info[2]}\n'
            f'*Фамилия:* {info[3]}\n'
            f'*Возраст:* {info[4]}\n'
            f'*Почта:* {info[5]}\n'
            f'*Номер телефона:* {info[6]}\n'
            f'*Язык:* {info[10]}\n'
            f'*Реферальная ссылка:* `https://t.me/rezak_tvorec_bot?start={message.from_user.id}`')
    text_eng = (f'You have entered the "Settings" section.\n'
            f'Here you can fill in your personal information.\n'
            f'*Name:* {info_eng[2]}\n'
            f'*Surname:* {info_eng[3]}\n'
            f'*Age:* {info_eng[4]}\n'
            f'*E-mail:* {info_eng[5]}\n'
            f'*Phone number:* {info_eng[6]}\n'
            f'*Language:* {info_eng[10]}\n'
            f'*Referral link:* `https://t.me/Expert_tgbot?start={message.from_user.id}`')
    if lang == 'EN':
        await bot.send_message(chat_id=message.from_user.id, text=text_eng,
                               reply_markup=settings(int(list(*db.user_politics(message.from_user.id))[0]), lang),
                               parse_mode=ParseMode.MARKDOWN)
    else:
        await bot.send_message(chat_id=message.from_user.id, text=text,
                               reply_markup=settings(int(list(*db.user_politics(message.from_user.id))[0]), lang),
                               parse_mode=ParseMode.MARKDOWN)

@sett.callback_query(F.data == 'setdestroy')
async def settings_destroy(call: CallbackQuery):
    await call.message.delete()

@sett.callback_query(F.data.startswith('lang'))
async def settings_destroy(call: CallbackQuery, bot: Bot):
    language = call.data[-2:]
    db.user_update_language(language, call.from_user.id)
    lang = list(*db.get_lang(call.from_user.id))[0]
    info = [x if x != None else 'Отсутствует' for x in list(*db.get_user(call.from_user.id))]
    info_eng = [x if x != None else 'Not found' for x in list(*db.get_user(call.from_user.id))]
    text = (f'Вы перешли в раздел "Настройки".\n'
            f'Здесь вы можете заполнить данные о себе.\n'
            f'*ID:* `{call.from_user.id}`\n'
            f'*Имя:* {info[2]}\n'
            f'*Фамилия:* {info[3]}\n'
            f'*Возраст:* {info[4]}\n'
            f'*Почта:* {info[5]}\n'
            f'*Номер телефона:* {info[6]}\n'
            f'*Язык:* {info[10]}\n'
            f'*Реферальная ссылка:* `https://t.me/rezak_tvorec_bot?start={call.from_user.id}`')
    text_eng = (f'You have entered the "Settings" section.\n'
            f'Here you can fill in your personal information.\n'
            f'*Name:* {info_eng[2]}\n'
            f'*Surname:* {info_eng[3]}\n'
            f'*Age:* {info_eng[4]}\n'
            f'*E-mail:* {info_eng[5]}\n'
            f'*Phone number:* {info_eng[6]}\n'
            f'*Language:* {info_eng[10]}\n'
            f'*Referral link:* `https://t.me/Expert_tgbot?start={call.from_user.id}`')
    if language == 'EN':
        try:
            await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=text_eng,
                                        reply_markup=settings(int(list(*db.user_politics(call.from_user.id))[0]), lang),
                                        parse_mode=ParseMode.MARKDOWN)
            await bot.send_message(chat_id=call.from_user.id, text='Language switched', reply_markup=keyboard_eng)
        except:
            await call.answer()
    else:
        try:
            await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=text,
                                        reply_markup=settings(int(list(*db.user_politics(call.from_user.id))[0]), lang),
                                        parse_mode=ParseMode.MARKDOWN)

            await bot.send_message(chat_id=call.from_user.id, text='Язык изменен', reply_markup=keyboard)
        except:
            await call.answer()
    db.commit()
    await call.answer()

@sett.callback_query(F.data == 'polit')
async def settings_get_name(call: CallbackQuery, bot: Bot):
    db.set_user_politics(call.from_user.id)
    await call.answer()
    lang = list(*db.get_lang(call.from_user.id))[0]
    info = [x if x != None else 'Отсутствует' for x in list(*db.get_user(call.from_user.id))]
    await bot.send_message(text = f'Вы перешли в раздел "Настройки".\n'
                                f'Здесь вы можете заполнить данные о себе.\n'
                                f'*ID:* `{call.from_user.id}`\n'
                                f'*Имя:* {info[2]}\n'
                                f'*Фамилия:* {info[3]}\n'
                                f'*Возраст:* {info[4]}\n'
                                f'*Почта:* {info[5]}\n'
                                f'*Номер телефона:* {info[6]}\n'
                                f'*Язык:* {info[10]}\n'
                                f'*Реферальная ссылка:* `https://t.me/rezak_tvorec_bot?start={call.from_user.id}`', chat_id=call.from_user.id, reply_markup=settings(int(list(*db.user_politics(call.from_user.id))[0]), lang), parse_mode=ParseMode.MARKDOWN)

@sett.callback_query(F.data == 'name/last')
async def settings_get_name(call: CallbackQuery, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(call.from_user.id))[0]
    if lang == 'RU':
        await bot.send_message(chat_id=call.from_user.id, text='Напишите имя и фамилию:')
        await bot.send_message(text = 'Нажмите на кнопку для отмены', reply_markup=deactivate, chat_id=call.from_user.id)
    else:
        await bot.send_message(chat_id=call.from_user.id, text='Write your first and last name:')
        await bot.send_message(text = 'Click on the button to cancel', reply_markup=deactivate_eng, chat_id=call.from_user.id)
    await state.set_state(settings_user.settings_name)
    await call.answer()

@sett.message(settings_user.settings_name)
async def get_info_name(message: Message, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(message.from_user.id))[0]
    try:
        first_name, last_name = message.text.split()
        db.user_update(first_name, last_name, message.from_user.username, message.from_user.id)
        if lang == 'RU':
            await bot.send_message(text='Спасибо что поделились!', reply_markup=keyboard, chat_id=message.user.id)
        else:
            await bot.send_message(text='Thank you for answer', reply_markup=keyboard_eng, chat_id=message.user.id)
        await state.clear()
        db.commit()
    except:
        if lang == 'RU':
            await bot.send_message(chat_id=message.from_user.id, text='Напишите имя и фамилию:')
            await bot.send_message(text='Нажмите на кнопку для отмены', reply_markup=deactivate,
                                   chat_id=message.from_user.id)
        else:
            await bot.send_message(chat_id=message.from_user.id, text='Write your first and last name:')
            await bot.send_message(text='Click on the button to cancel', reply_markup=deactivate_eng,
                                   chat_id=message.from_user.id)
        await state.set_state(settings_user.settings_name)

@sett.callback_query(F.data == 'age')
async def settings_get_age(call: CallbackQuery, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(call.from_user.id))[0]
    if lang == 'RU':
        await bot.send_message(chat_id=call.from_user.id, text='Напишите ваш возраст:')
        await bot.send_message(text='Нажмите на кнопку для отмены', reply_markup=deactivate,
                               chat_id=call.from_user.id)
    else:
        await bot.send_message(chat_id=call.from_user.id, text='Write your age:')
        await bot.send_message(text='Click on the button to cancel', reply_markup=deactivate_eng,
                               chat_id=call.from_user.id)
    await state.set_state(settings_user.settings_age)
    await call.answer()

@sett.message(settings_user.settings_age)
async def get_info_age(message: Message, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(message.from_user.id))[0]
    try:
        age = int(message.text)
        db.user_update_age(age, message.from_user.id)
        if lang == 'RU':
            await bot.send_message(text='Спасибо что поделились!', reply_markup=keyboard, chat_id=message.user.id)
        else:
            await bot.send_message(text='Thank you for answer', reply_markup=keyboard_eng, chat_id=message.user.id)
        await state.clear()
        db.commit()
    except:
        if lang == 'RU':
            await bot.send_message(chat_id=message.from_user.id, text='Напишите ваш возраст:')
            await bot.send_message(text='Нажмите на кнопку для отмены', reply_markup=deactivate,
                                   chat_id=message.from_user.id)
        else:
            await bot.send_message(chat_id=message.from_user.id, text='Write your age:')
            await bot.send_message(text='Click on the button to cancel', reply_markup=deactivate_eng,
                                   chat_id=message.from_user.id)
        await state.set_state(settings_user.settings_age)

@sett.callback_query(F.data == 'email')
async def settings_get_email(call: CallbackQuery, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(call.from_user.id))[0]
    if lang == 'RU':
        await bot.send_message(chat_id=call.from_user.id, text='Напишите вашу электронную почту:')
        await bot.send_message(text='Нажмите на кнопку для отмены', reply_markup=deactivate,
                               chat_id=call.from_user.id)
    else:
        await bot.send_message(chat_id=call.from_user.id, text='Write your e-mail:')
        await bot.send_message(text='Click on the button to cancel', reply_markup=deactivate_eng,
                               chat_id=call.from_user.id)
    await state.set_state(settings_user.settings_email)
    await call.answer()

@sett.message(settings_user.settings_email)
async def get_info_email(message: Message, state: FSMContext, bot: Bot):
    data = {"email": "<N/A>",}
    entities = message.entities or []
    lang = list(*db.get_lang(message.from_user.id))[0]
    for item in entities:
        if item.type in data.keys():
            data[item.type] = item.extract_from(message.text)
    if 'N/A' in data['email']:
        if lang == 'RU':
            await bot.send_message(chat_id=message.from_user.id, text='Напишите вашу электронную почту:')
            await bot.send_message(text='Нажмите на кнопку для отмены', reply_markup=deactivate,
                                   chat_id=message.from_user.id)
        else:
            await bot.send_message(chat_id=message.from_user.id, text='Write your e-mail:')
            await bot.send_message(text='Click on the button to cancel', reply_markup=deactivate_eng,
                                   chat_id=message.from_user.id)
        await state.set_state(settings_user.settings_email)
    else:
        db.user_update_email(data['email'], message.from_user.id)
        if lang == 'RU':
            await bot.send_message(text='Спасибо что поделились!', reply_markup=keyboard, chat_id=message.user.id)
        else:
            await bot.send_message(text='Thank you for answer', reply_markup=keyboard_eng, chat_id=message.user.id)
        await state.clear()
        db.commit()

@sett.callback_query(F.data == 'phone')
async def settings_get_phone(call: CallbackQuery, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(call.from_user.id))[0]
    if lang == 'RU':
        await bot.send_message(chat_id=call.from_user.id, text='Отправьте ваш номер телефона:', reply_markup=phone)
        await bot.send_message(text='Нажмите на кнопку для отмены', reply_markup=deactivate,
                               chat_id=call.from_user.id)
    else:
        await bot.send_message(chat_id=call.from_user.id, text='Write your e-mail:')
        await bot.send_message(text='Click on the button to cancel', reply_markup=deactivate_eng,
                               chat_id=call.from_user.id)
    await state.set_state(settings_user.settings_number)
    await call.answer()

@sett.message(settings_user.settings_number)
async def get_info_phone(message: Message, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(message.from_user.id))[0]
    try:
        phone_num = str(message.contact).split()[0][14:-1]
        db.user_update_phone_number(phone_num, message.from_user.id)
        if lang == 'RU':
            await bot.send_message(text='Спасибо что поделились!', reply_markup=keyboard, chat_id=message.user.id)
        else:
            await bot.send_message(text='Thank you for answer', reply_markup=keyboard_eng, chat_id=message.user.id)
        await state.clear()
        db.commit()
    except:
        if lang == 'RU':
            await bot.send_message(chat_id=message.from_user.id, text='Отправьте ваш номер телефона:', reply_markup=phone)
            await bot.send_message(text='Нажмите на кнопку для отмены', reply_markup=deactivate,
                                   chat_id=message.from_user.id)
        else:
            await bot.send_message(chat_id=message.from_user.id, text='Write your phone number:', reply_markup=phone)
            await bot.send_message(text='Click on the button to cancel', reply_markup=deactivate_eng,
                                   chat_id=message.from_user.id)
        await state.set_state(settings_user.settings_number)

@sett.callback_query(F.data == 'poll')
async def settings_get_poll(call: CallbackQuery, bot: Bot):
    lang = list(*db.get_lang(call.from_user.id))[0]
    if lang == 'RU':
        options = ['Социальные сети 🔗', 'Поисковая выдача 🔎', 'Рекомендация друзей 😉', 'Из рекламы 📝', 'E-mail рассылка 📩']
    else:
        options = ['Social media 🔗', 'Search 🔎', 'Recommendation from friends 😉', 'Advertising 📝', 'Mailing 📩']
    await bot.send_poll(chat_id=call.from_user.id, question='Откуда вы узнали про компанию ТВОРЕЦ?',
                        options=options,
                        open_period=30,
                        is_anonymous=False,
                        allows_multiple_answers=True)
    await call.answer()

@sett.poll_answer()
async def settings_get_poll_answer(poll: PollAnswer, bot: Bot):
    db.user_update_spawn(' '.join([str(x) for x in poll.option_ids]), poll.user.id)
    db.commit()
    lang = list(*db.get_lang(poll.user.id))[0]
    if lang == 'RU':
        await bot.send_message(text='Спасибо что поделились!', reply_markup=keyboard, chat_id=poll.user.id)
    else:
        await bot.send_message(text='Thank you for answer', reply_markup=keyboard_eng, chat_id=poll.user.id)

