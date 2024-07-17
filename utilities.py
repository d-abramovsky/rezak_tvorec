from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.utils.markdown import hlink
from commands import set_commands
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters.command import Command
from database import Database
from reply_keyboard import keyboard, rezak, keyboard_eng, rezak_eng
from config import superuser
from aiogram import F, Bot, Router
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from inline_keyboard import web, gos
import pygsheets
from telegraph import Telegraph

db = Database('db.db')
ut = Router()


path = 'service_account_spreadsheets.json'
gc = pygsheets.authorize(service_account_file=path)
sh = gc.open('Rezak Tvorec')
wk = sh[0]


@ut.startup()
async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(superuser, text='Бот запущен!')

@ut.shutdown()
async def stop_bot(bot: Bot):
    await bot.send_message(superuser, text='Бот остановлен!')

@ut.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated):
    db.user_set_active('0', event.from_user.id)
    db.commit()

@ut.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated):
    db.user_set_active('1', event.from_user.id)
    db.commit()

@ut.message(Command('reset_calculator'))
async def reset(message: Message):
    web_land = hlink('Вот ваша старая страница',
                 f'{list(*db.get_telegraph(user_id=message.from_user.id))[0]}')
    await message.answer(text=f'Понял, сейчас удалю!\n'
                              f'{web_land}')
    telegraph = Telegraph("998586d4f006c54996d913c05f80de870496add70e1bf19199d2cce12416")
    response = telegraph.create_page(
        f'{message.from_user.first_name}, это страница со всеми рассчетами',
        html_content='<p>Статистика работ:</p>')
    db.add_telegraph('https://telegra.ph/{}'.format(response['path']), message.from_user.id)

@ut.message(Command('commands'))
async def reset(message: Message):
    admins = [str(db.get_admins()[x][0]) for x in range(len(db.get_admins()))]
    if str(message.from_user.id) in admins:
        await message.answer(text='/admins - администраторы\n'
                                  '/change_section - изменение подразделов\n'
                                  '/mailing - рассылка\n'
                                  '/watchmailing - архив рассылок\n'
                                  '/reset_calculator - сброс страницы калькуляций\n'
                                  '/statistics - просмотр статистики\n'
                                  '/archive_database - архивирование базы даннях\n'
                                  'new_admin + user_id - добавление админа (нужно написать id пользователя)\n'
                                  'delete_admin + user_id - добавление админа (нужно написать id пользователя)', parse_mode=ParseMode.MARKDOWN)

@ut.message(Command('start'))
async def start(message: Message, bot: Bot):
    username = message.from_user.username
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    db.add_statistics(message.from_user.id, message.text, str(message.date)[:-15], str(message.date)[-14:-6])
    referral_id = message.text[7:]
    if not db.user_exists(message.from_user.id):
        db.add_user(user_id, first_name, last_name, username)
        if referral_id != '':
            if referral_id != message.from_user.id:
                web = f'https://t.me/{list(*db.get_username(referral_id))[0]}'
                await message.answer(text=f'Добро пожаловать в официальный телеграм канал компании ТВОРЕЦ.\n'
                                          f'Вы были приглашены по ссылке пользователя {hlink(list(*db.get_user_firstname(referral_id))[0], web)}', disable_web_page_preview=True)
                db.referrals(referral_id, message.from_user.id, str(message.date)[:-15], str(message.date)[-14:-6])
                db.commit()
            else:
                await message.answer(text = 'Нельзя регестрироваться по собственной ссылке')
        telegraph = Telegraph("998586d4f006c54996d913c05f80de870496add70e1bf19199d2cce12416")
        response = telegraph.create_page(
            f'{first_name}, это страница со всеми рассчетами',
            html_content='<p>Статистика работ:</p>')
        db.add_telegraph('https://telegra.ph/{}'.format(response['path']), user_id)
    elif db.user_exists(message.from_user.id):
        db.user_update(first_name, last_name, username, user_id)
    founder = 'https://www.rezak-penoplasta-tvorec.ru/wp-content/uploads/2022/04/founder.jpg'
    language = list(*db.get_lang(message.from_user.id))[0]
    if message.from_user.id == superuser:
        if language == 'RU':
            await bot.send_photo(chat_id=message.from_user.id, photo=founder,
                                 caption=f'Добрый день, {message.from_user.first_name}!\nЯ-консультант Антон. Чем могу тебе помочь?',
                                 reply_markup=keyboard)
        else:
            await bot.send_photo(chat_id=message.from_user.id, photo=founder,
                                 caption=f"Hello {message.from_user.first_name}! I'm Anton the consultant. What can I do for you?",
                                 reply_markup=keyboard_eng)
    else:
        if language == 'RU':
            await bot.send_photo(chat_id=message.from_user.id, photo=founder,
                                 caption=f'Добрый день, {message.from_user.first_name}!\nЯ-консультант Антон. Чем могу тебе помочь?',
                                 reply_markup=keyboard)
        else:
            await bot.send_photo(chat_id=message.from_user.id, photo=founder,
                                 caption=f"Hello {message.from_user.first_name}! I'm Anton the consultant. What can I do for you?",
                                 reply_markup=keyboard_eng)
    db.commit()


@ut.message(Command('about'))
async def about(message: Message):
    await message.answer(
        text='Добро пожаловать в телеграм-бот компании ТВОРЕЦ – первого российского производителя инструментов для стайрофоминга.'
             '\n\nЭтот бот поможет вам ориентироваться в широком ассортименте нашего бренда, а также познакомит вас с цифровыми продуктами компаний ТВОРЕЦ и Академии стайрофоминга.'
             '\n\nУспехов в творчестве, друзья!',
        reply_markup=web)
@ut.message(F.text == 'Вернуться в главное меню')
async def back(message: Message):
    if message.from_user.id ==superuser:
        await message.answer(text='Вы вернулись в главное меню', reply_markup=keyboard)
    else:
        await message.answer(text = 'Вы вернулись в главное меню', reply_markup=keyboard)

@ut.message(F.text == 'Госучреждениям')
async def back(message: Message):
    await message.answer(text='Благодаря инструментам для стайрофоминга торговой марки «ТВОРЕЦ» воспитатели детских садов могут с легкостью создавать оригинальный декор к мероприятиям и развивающие материалы для занятий.\n'
                              'Компания “ТВОРЕЦ” работает с детскими садами по безналичному расчету, предоставляя все необходимые закрывающие документы.\n'
                              'Вы можете купить резаки пенопласта для детского сада по ценам от производителя.', reply_markup=gos)

@ut.message(F.text == 'Назад')
async def back_choice(message: Message):
    builder = ReplyKeyboardBuilder()
    builder.attach(ReplyKeyboardBuilder.from_markup(rezak))
    admin_builder = ReplyKeyboardBuilder()
    if message.from_user.id == superuser:
        admin_builder.button(text='Добавить новый раздел')
        admin_builder.button(text='Удалить раздел')
        admin_builder.adjust(2)
    builder.attach(admin_builder)
    await message.answer(text='Вы вернулись назад',reply_markup=builder.as_markup(resize_keyboard=True),)

@ut.message(F.text == 'Return to the main menu')
async def back_choice(message: Message):
    await message.answer(text='You are back at the main menu',reply_markup=keyboard_eng,)

@ut.message(F.text == 'Go back')
async def back_choice(message: Message):
    await message.answer(text='You came back',reply_markup=rezak_eng,)

@ut.message(F.text == 'Смотреть другие цифровые продукты')
async def back_choice(message: Message):
    builder = ReplyKeyboardBuilder()
    builder.button(text='Стайрофоминг-проект')
    builder.button(text='Мастер-класс')
    builder.button(text='Онлайн-курс')
    builder.button(text='Вернуться в главное меню')
    builder.adjust(1)
    await message.answer(text='Изучите другие цифровые продукты!',reply_markup=builder.as_markup(resize_keyboard=True),)

@ut.callback_query(F.data == 'finish_state')
async def deact_state(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.send_message(chat_id=call.from_user.id, text='Отменено' , reply_markup=keyboard)
    await state.clear()
    await call.answer()
    await call.message.delete()

@ut.callback_query(F.data == 'finish_state_eng')
async def deact_state_eng(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.send_message(chat_id=call.from_user.id, text='Canceled' , reply_markup=keyboard)
    await state.clear()
    await call.answer()
    await call.message.delete()
