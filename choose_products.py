from aiogram import Router, F, Bot
from aiogram.types import Message, InputMediaPhoto, CallbackQuery
from database import Database
from config import superuser
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from reply_keyboard import rezak, skip, rezak_eng, keyboard
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext
from inline_keyboard import confirm, photo, delete, update_product, deactivate

db = Database('db.db')
cut = Router()

class new_card(StatesGroup):
    add_name = State()
    add_description = State()
    add_photo = State()
    photo_link = State()
    upload_photo = State()
    add_buttons = State()
    finish_card = State()
    changed = State()
    photo_change = State()

class del_card(StatesGroup):
    conf_del = State()

class new_header(StatesGroup):
    get_header = State()
    get_group = State()
    delete_header = State()

class update_card(StatesGroup):
    start_update_card = State()
    finish_update_card = State()


@cut.message(F.text.in_({'Выбрать резаки', 'Choose cutters'}))
async def choice(message:Message, bot: Bot):
    db.add_statistics(message.from_user.id, message.text, str(message.date)[:-15], str(message.date)[-14:-6])
    db.commit()
    path = 'https://www.rezak-penoplasta-tvorec.ru/wp-content/uploads/2022/03/%D0%BC%D0%B8%D1%80-%D1%82%D0%B2%D0%BE%D1%80%D1%86%D0%B0.jpg'
    builder = ReplyKeyboardBuilder()
    if message.text == 'Выбрать резаки':
        builder.attach(ReplyKeyboardBuilder.from_markup(rezak))
        await bot.send_photo(chat_id=message.from_user.id, photo=path, reply_markup=builder.as_markup(resize_keyboard=True), caption =
        'Какой тип резки планируется?'
        '\n<b>Художественная резка</b> - объемные цифры, буквы, виньетки,фигуры'
        '\n<b>Техническая резка</b> - простые геометрические формы для различных целей')
    else:
        builder.attach(ReplyKeyboardBuilder.from_markup(rezak_eng))
        await bot.send_photo(chat_id=message.from_user.id, photo=path, reply_markup=builder.as_markup(resize_keyboard=True), caption =
                             'What type of cutting is planned?\n'
                             'Artistic cutting - three-dimensional numbers, letters, vignettes, figures.\n'
                             'Technical cutting - simple geometric shapes for various purposes.')

@cut.message(F.text.in_({'Выбрать аксессуары', 'Choose accessories'}))
async def artistic(message: Message):
    db.add_statistics(message.from_user.id, message.text, str(message.date)[:-15], str(message.date)[-14:-6])
    db.commit()
    builder = ReplyKeyboardBuilder()
    a = [x[0] for x in db.topic('Выбрать аксессуары')]
    if message.text == 'Выбрать аксессуары':
        for i in a:
            builder.button(text='•' + ' ' + str(i))
        builder.button(text='Вернуться в главное меню')
        builder.adjust(1)
        await message.answer(text=f'Для чего вам необходимы аксессуары?',
                         reply_markup=builder.as_markup(resize_keyboard=True))
    else:
        for i in a:
            builder.button(text='•' + ' ' + str(list(*db.get_translation(i))[0]))
        builder.button(text='Return to the main menu')
        builder.adjust(1)
        await message.answer(text=f'What accessories do you need?',
                         reply_markup=builder.as_markup(resize_keyboard=True))

@cut.message(F.text == 'Выбрать цифровые продукты')
async def artistic(message: Message):
    db.add_statistics(message.from_user.id, message.text, str(message.date)[:-15], str(message.date)[-14:-6])
    db.commit()
    builder = ReplyKeyboardBuilder()
    builder.button(text='Стайрофоминг-проект')
    builder.button(text='Мастер-класс')
    builder.button(text='Онлайн-курс')
    builder.button(text='Вернуться в главное меню')
    builder.adjust(1)
    await message.answer(text=f'Какие цифровые продукты вам нужны?',
                         reply_markup=builder.as_markup(resize_keyboard=True))

@cut.message(F.text == 'Онлайн-курс')
async def artistic(message: Message):
    db.add_statistics(message.from_user.id, message.text, str(message.date)[:-15], str(message.date)[-14:-6])
    db.commit()
    builder = ReplyKeyboardBuilder()
    a = [x[0] for x in db.topic('Онлайн-курс')]
    for i in a:
        builder.button(text='•' + ' ' + str(i))
    builder.button(text='Смотреть другие цифровые продукты')
    builder.button(text='Вернуться в главное меню')
    builder.adjust(1)
    await message.answer(text=f'Какой онлайн-курс вы хотите?',
                         reply_markup=builder.as_markup(resize_keyboard=True))

@cut.message(F.text == 'Мастер-класс')
async def artistic(message: Message):
    db.add_statistics(message.from_user.id, message.text, str(message.date)[:-15], str(message.date)[-14:-6])
    db.commit()
    builder = ReplyKeyboardBuilder()
    a = [x[0] for x in db.topic('Мастер-класс')]
    for i in a:
        builder.button(text='•' + ' ' + str(i))
    builder.button(text='Смотреть другие цифровые продукты')
    builder.button(text='Вернуться в главное меню')
    builder.adjust(1)
    await message.answer(text=f'Какой мастер-класс вы хотите?',
                         reply_markup=builder.as_markup(resize_keyboard=True))

@cut.message(F.text == 'Стайрофоминг-проект')
async def artistic(message: Message):
    db.add_statistics(message.from_user.id, message.text, str(message.date)[:-15], str(message.date)[-14:-6])
    db.commit()
    builder = ReplyKeyboardBuilder()
    a = [x[0] for x in db.topic('Стайрофоминг-проект')]
    for i in a:
        builder.button(text='•' + ' ' + str(i))
    builder.button(text='Смотреть другие цифровые продукты')
    builder.button(text='Вернуться в главное меню')
    builder.adjust(1)
    await message.answer(text=f'Какой стайрофоминг-проект вы хотите?',
                         reply_markup=builder.as_markup(resize_keyboard=True))

@cut.message(F.text.in_({'Выбрать расходные материалы', 'Choose consumables'}))
async def artistic(message: Message):
    db.add_statistics(message.from_user.id, message.text, str(message.date)[:-15], str(message.date)[-14:-6])
    db.commit()
    builder = ReplyKeyboardBuilder()
    a = [x[0] for x in db.topic('Выбрать расходные материалы')]
    if message.text == 'Выбрать расходные материалы':
        for i in a:
            builder.button(text='•' + ' ' + str(i))
        builder.button(text='Вернуться в главное меню')
        builder.adjust(1)
        await message.answer(text=f'Какой у вас Творец?',
                             reply_markup=builder.as_markup(resize_keyboard=True))
    else:
        for i in a:
            builder.button(text='•' + ' ' + str(list(*db.get_translation(i))[0]))
        builder.button(text='Return to the main menu')
        builder.adjust(1)
        await message.answer(text=f'What model of cutter do you have?',
                         reply_markup=builder.as_markup(resize_keyboard=True))



@cut.message(F.text.in_({'Художественная резка', 'Artistic cutting'}))
async def artistic(message: Message):
    db.add_statistics(message.from_user.id, message.text, str(message.date)[:-15], str(message.date)[-14:-6])
    db.commit()
    builder = ReplyKeyboardBuilder()
    a = [x[0] for x in db.topic('Художественная резка')]
    if message.text == 'Художественная резка':
        for i in a:
            builder.button(text='•' + ' ' + str(i))
        builder.button(text='Назад')
        builder.button(text='Вернуться в главное меню')
        builder.adjust(1)
        await message.answer(text=f'Для каких задач вам нужен резак?',
                             reply_markup=builder.as_markup(resize_keyboard=True))
    else:
        for i in a:
            builder.button(text='•' + ' ' + str(list(*db.get_translation(i))[0]))
        builder.button(text='Go back')
        builder.button(text='Return to the main menu')
        builder.adjust(1)
        await message.answer(text=f'What tasks do you need a cutter for?',
                         reply_markup=builder.as_markup(resize_keyboard=True))

@cut.message(F.text.in_({'Техническая резка', 'Technical cutting'}))
async def technic(message: Message):
    db.add_statistics(message.from_user.id, message.text, str(message.date)[:-15], str(message.date)[-14:-6])
    db.commit()
    builder = ReplyKeyboardBuilder()
    a = [x[0] for x in db.topic('Техническая резка')]
    if message.text == 'Техническая резка':
        for i in a:
            builder.button(text='•' + ' ' + str(i))
        builder.button(text='Назад')
        builder.button(text='Вернуться в главное меню')
        builder.adjust(1)
        await message.answer(text=f'Для каких задач вам нужен резак?',
                             reply_markup=builder.as_markup(resize_keyboard=True))
    else:
        for i in a:
            builder.button(text='•' + ' ' + str(list(*db.get_translation(i))[0]))
        builder.button(text='Go back')
        builder.button(text='Return to the main menu')
        builder.adjust(1)
        await message.answer(text=f'What tasks do you need a cutter for?',
                         reply_markup=builder.as_markup(resize_keyboard=True))

@cut.message(F.text.startswith('•'))
async def topic(message: Message, bot: Bot, state: FSMContext):
    db.add_statistics(message.from_user.id, message.text, str(message.date)[:-15], str(message.date)[-14:-6])
    db.commit()
    key = message.text[2:]
    if list(*db.get_lang(message.from_user.id))[0] == 'EN':
        inform = db.name(list(*db.get_en_translation(key))[0])
    else:
        inform = db.name(key)
    db.commit()
    if len(inform) == 0 and message.from_user.id == superuser:
        if message.from_user.id == superuser:
            await message.answer(text = 'Похоже, в этом разделе нет карточек. Давайте ее создадим!\n'
                                        'Напишите название:')
            await state.update_data(label = db.get_label(key)[0])
            await state.update_data(id = key)
            uinn = db.uin()
            uin_list = [int(uinn[x][0]) for x in range(len(list(db.uin())))]
            for i in range(100, 1000):
                if i not in uin_list:
                    await state.update_data(uin=i)
                    break
            await state.update_data(previous='Начало')
            await state.update_data(next='Конец')
            await state.update_data(new_add='1')
            await message.answer(text='Нажмите на кнопку для отмены', reply_markup=deactivate)
            await state.set_state(new_card.add_name)
        else:
            if list(*db.get_lang(message.from_user.id))[0] == 'RU':
                await message.answer(text = 'Похоже, в этом разделе нет карточек☹️')

            else:
                await message.answer(text = 'There are no cards in this section ☹️')
    else:
        id, uin, label, name, description, prv, nxt, photo, file_id, link, text_link = list(*inform)
        link = str(link).split()
        text_link = str(text_link).split('|')
        builder = InlineKeyboardBuilder()
        if link[0] != 'Нет':
            if list(*db.get_lang(message.from_user.id))[0] == 'EN':
                for i in range(len(link)):
                    builder.button(text=list(*db.get_translation(text_link[i]))[0],
                                   url=link[i])
            else:
                for i in range(len(link)):
                    builder.button(text=text_link[i], url=link[i])
        if list(*db.get_lang(message.from_user.id))[0] == 'EN':
            caption = (f'{list(*db.get_translation(name))[0]}\n'
                       f'Click the button below to find out more')
        else:
            caption = f'{name}\n{description}'
        if (prv == 'Начало') and (nxt == 'Конец'):
            pass
        else:
            if list(*db.get_lang(message.from_user.id))[0] == 'EN':
                builder.button(text='Next', callback_data=nxt)
            else:
                builder.button(text='Смотреть дальше', callback_data=nxt)
        builder.adjust(1)
        if (int(message.from_user.id) == superuser and list(*db.get_lang(message.from_user.id))[0] == 'RU') or \
                (str(message.from_user.id) in [str(db.get_admin_id_menu()[x][0]) for x in range(len(db.get_admin_id_menu()))] and list(*db.get_lang(message.from_user.id))[0] == 'RU'):
            page = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Добавить следующую карту", callback_data=f'nc{label}{uin}'),
                    ],
                    [
                        InlineKeyboardButton(text="Изменить текущую карту", callback_data=f'cpch{uin}'),
                    ],
                ],
            )
            builder.attach(InlineKeyboardBuilder.from_markup(page))
        if photo!= '0':
            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=photo,
                                 caption=caption,
                                 reply_markup=builder.as_markup())
        else:
            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=file_id,
                                 caption=caption,
                                 reply_markup=builder.as_markup())
    db.commit()

@cut.callback_query(F.data.startswith('cpch'))
async def product_update_card(call: CallbackQuery, state: FSMContext, bot: Bot):
    uin = call.data[-3:]
    await bot.send_message(chat_id=call.from_user.id, text = 'Что будем изменять?', reply_markup=update_product)
    await bot.send_message(text = 'Нажмите на кнопку для отмены', reply_markup=deactivate, chat_id=call.from_user.id)
    await call.answer()
    await state.update_data(uin = uin)
    await state.set_state(update_card.start_update_card)

@cut.callback_query(update_card.start_update_card, F.data == "name_change")
async def name_change(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text = 'Отправьте новое название:', chat_id=call.from_user.id)
    await call.answer()
    await state.update_data(change = 'name')
    await state.set_state(update_card.finish_update_card)

@cut.callback_query(update_card.start_update_card, F.data == "description_change")
async def name_change(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text = 'Отправьте новое описание:', chat_id=call.from_user.id)
    await call.answer()
    await state.update_data(change = 'description')
    await state.set_state(update_card.finish_update_card)

@cut.callback_query(update_card.start_update_card, F.data == "photo_change")
async def photo_change(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text = 'Отправьте новую фотографию:\n'
                                  '(Это может быть как файл, так и ссылка)', chat_id=call.from_user.id)
    await call.answer()
    await state.update_data(change = 'photo')
    await state.set_state(update_card.finish_update_card)

@cut.callback_query(update_card.start_update_card, F.data == "button_change")
async def button_change(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text = f'Отправьте измененные кнопки:'
                                f'\nПример сообщения: Ссылка_на_материал текст_кнопки'
                                f'\nМежду ссылкой и текстом кнопки должен быть |'
                                f'\nЕсли кнопок нет, нажмите кнопку', chat_id=call.from_user.id, reply_markup=skip)
    await call.answer()
    await state.update_data(change = 'button')
    await state.set_state(update_card.finish_update_card)

@cut.message(update_card.finish_update_card)
async def final_update(message: Message, state: FSMContext):
    context_data = await state.get_data()
    change = context_data.get('change')
    uin = context_data.get('uin')
    if change == 'name':
        db.product_update_name(message.text, uin)
        await message.answer(text = 'Название изменено успешно!')
    elif change == 'photo':
        if message.photo:
            db.product_update_file_id(message.photo[-1].file_id, uin)
        else:
            db.product_update_photo(message.text, uin)
        await message.answer(text = 'Фотографя изменена успешно!')
    elif change == 'button':
        button = message.text.split('|')
        if len(button) == 1:
            link = text_link = 'Нет'
        else:
            link = ' '.join([button[x] for x in range(len(button)) if x % 2 == 0])
            text_link = '|'.join([button[x] for x in range(len(button)) if x % 2 != 0])
        db.product_update_buttons(link, text_link, uin)
    else:
        db.product_update_name(message.text, uin)
        await message.answer(text = 'Описание изменено успешно!')
    db.commit()
    await state.clear()


@cut.callback_query(F.data.startswith('$'))
async def call_topic(call: CallbackQuery, bot: Bot):
    key = call.data[2:].strip()
    inform = db.call_name(key)
    id, uin, label, name, description, prv, nxt, photo, file_id, link, text_link = list(*inform)
    db.commit()
    link = str(link).split()
    text_link = str(text_link).split('|')
    builder = InlineKeyboardBuilder()
    if link[0] != 'Нет':
        if list(*db.get_lang(call.from_user.id))[0] == 'EN':
            for i in range(len(link)):
                builder.button(text=list(*db.get_translation(text_link[i]))[0],
                               url=link[i])
        else:
            for i in range(len(link)):
                builder.button(text=text_link[i], url=link[i])
    if list(*db.get_lang(call.from_user.id))[0] == 'EN':
        caption = (f'{list(*db.get_translation(name))[0]}\n'
                   f'Click the button below to find out more')
    else:
        caption = f'{name}\n{description}'
    if nxt == 'Конец':
        if list(*db.get_lang(call.from_user.id))[0] == 'EN':
            builder.button(text='Back', callback_data=prv)
        else:
            builder.button(text='Вернуться назад', callback_data=prv)
        builder.adjust(1)
    elif prv == 'Начало':
        if list(*db.get_lang(call.from_user.id))[0] == 'EN':
            builder.button(text='Next', callback_data=nxt)
        else:
            builder.button(text='Смотреть дальше', callback_data=nxt)
        builder.adjust(1)
    else:
        if list(*db.get_lang(call.from_user.id))[0] == 'EN':
            page = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Back', callback_data=prv),
                        InlineKeyboardButton(text='Next', callback_data=nxt)
                    ],
                ],
            )
        else:
            page = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Вернуться назад', callback_data=prv),
                        InlineKeyboardButton(text='Смотреть дальше', callback_data=nxt)
                    ],
                ],
            )
        builder.adjust(1)
        builder.attach(InlineKeyboardBuilder.from_markup(page))
    if (int(call.from_user.id) == superuser and list(*db.get_lang(call.from_user.id))[0] == 'RU') or \
            (str(call.from_user.id) in [str(db.get_admin_id_menu()[x][0]) for x in range(len(db.get_admin_id_menu()))] and list(*db.get_lang(call.from_user.id))[0] == 'RU'):
        if prv == 'Начало':
            page = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Добавить следующую карту", callback_data=f'nc{label}{uin}'),
                    ],
                    [
                        InlineKeyboardButton(text="Изменить текущую карту", callback_data=f'cpch{uin}'),
                    ],
                ],
            )
            builder.attach(InlineKeyboardBuilder.from_markup(page))
        else:
            page = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Добавить следующую карту", callback_data=f'nc{label}{uin}'),
                    ],
                    [
                        InlineKeyboardButton(text="Изменить текущую карту", callback_data=f'cpch{uin}'),
                    ],
                    [
                        InlineKeyboardButton(text="Удалить текущую карту", callback_data=f'dl{uin}{nxt}{prv}')
                    ],
                ],
            )
            builder.attach(InlineKeyboardBuilder.from_markup(page))
    if photo!= '0':
        await bot.edit_message_media(media=InputMediaPhoto(
            media=photo,
            caption=caption), chat_id=call.message.chat.id,
            message_id=call.message.message_id, reply_markup=builder.as_markup())
    else:
        await bot.edit_message_media(media=InputMediaPhoto(
            media=file_id,
            caption=caption), chat_id=call.message.chat.id,
            message_id=call.message.message_id, reply_markup=builder.as_markup())
    await call.answer()


@cut.callback_query(F.data.startswith('dl'))
async def delete_card(call: CallbackQuery, state: FSMContext, bot: Bot):
    if (int(call.from_user.id) == superuser and list(*db.get_lang(call.from_user.id))[0] == 'RU') or \
            (str(call.from_user.id) in [str(db.get_admin_id_menu()[x][0]) for x in range(len(db.get_admin_id_menu()))] and list(*db.get_lang(call.from_user.id))[0] == 'RU'):
        await state.update_data(prv = call.data[-5:])
        await state.update_data(nxt = call.data[-10:-5])
        await state.update_data(uin = call.data[-13:-10])
        await bot.send_message(chat_id=call.from_user.id, text = 'Вы точно хотите удалить карточку?', reply_markup= delete)
        await state.set_state(del_card.conf_del)
        await call.message.delete()
    await call.answer()

@cut.callback_query(del_card.conf_del, F.data == "del_1")
async def confirm_delete(call: CallbackQuery, state: FSMContext, bot: Bot):
    if (int(call.from_user.id) == superuser and list(*db.get_lang(call.from_user.id))[0] == 'RU') or \
            (str(call.from_user.id) in [str(db.get_admin_id_menu()[x][0]) for x in range(len(db.get_admin_id_menu()))] and list(*db.get_lang(call.from_user.id))[0] == 'RU'):
        context_data = await state.get_data()
        prv = context_data.get('prv')
        nxt = context_data.get('nxt')
        uin = context_data.get('uin')
        db.delete_1(nxt, prv[2:])
        db.delete_2(prv, nxt[2:])
        db.delete(uin)
        db.commit()
        await bot.send_message(chat_id=call.from_user.id, text = 'Этот мир не будет прежним. Я удалил эту карточку!')

    await state.clear()
    await call.message.delete()

@cut.callback_query(del_card.conf_del, F.data == "del_0")
async def close_delete(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await bot.send_message(chat_id=call.from_user.id, text = 'Все осталось на своих местах')
    await call.message.delete()

@cut.callback_query(F.data.startswith('nc'))
async def add_name(call: CallbackQuery, state: FSMContext, bot: Bot):
    if (int(call.from_user.id) == superuser and list(*db.get_lang(call.from_user.id))[0] == 'RU') or \
            (str(call.from_user.id) in [str(db.get_admin_id_menu()[x][0]) for x in range(len(db.get_admin_id_menu()))] and list(*db.get_lang(call.from_user.id))[0] == 'RU'):
        label = call.data[-4]
        if str(call.data[-5]) in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            label = call.data[-5:-3]
        else:
            label = call.data[-4]
        un =  call.data[-3:]
        await bot.send_message(text = 'Начинаем создание новой карточки \nНапишите название:', chat_id=call.from_user.id)
        await bot.send_message(text = 'Нажмите на кнопку для отмены', reply_markup=deactivate, chat_id=call.from_user.id)
        await state.set_state(new_card.add_name)
        await state.update_data(label = label)
        prv, nxt = list(*db.neighbours(un, label))
        await state.update_data(previous = prv)
        await state.update_data(next = nxt)
        await state.update_data(un = un)
        await state.update_data(new_add='0')
        uinn = db.uin()
        uin_list = [int(uinn[x][0]) for x in range(len(list(db.uin())))]
        for i in range(100, 1000):
            if i not in uin_list:
                await state.update_data(uin=i)
                break
        db.commit()
        await call.answer()

@cut.message(new_card.add_name)
async def add_description(message: Message, state: FSMContext):
    await message.answer(text=f'Напишите описание для карточки:')
    await state.update_data(name=message.text)
    await state.set_state(new_card.add_description)

@cut.message(new_card.add_description)
async def add_photo(message: Message, state: FSMContext):
    await message.answer(text=f'Как вы хотите загруить фотографию?', reply_markup=photo)
    await state.update_data(description=message.text)
    await state.set_state(new_card.add_photo)

@cut.callback_query(new_card.add_photo, F.data == "photo_link")
async def link(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text=f'Отправьте ссылку на фото для карточки', chat_id=call.from_user.id)
    await state.set_state(new_card.photo_link)
    await call.answer()

@cut.callback_query(new_card.add_photo, F.data == "upload_photo")
async def upload(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text=f'Отправьте фото для карточки', chat_id=call.from_user.id)
    await state.set_state(new_card.upload_photo)
    await call.answer()

@cut.message(new_card.photo_link)
async def add_link(message: Message, state: FSMContext):
    await message.answer(text=f'Отправьте материалы для кнопок:\n'
                              f'Пример сообщения: Ссылка_на_материал текст_кнопки\n'
                              f'<b>Между ссылкой и текстом кнопки должен быть |</b>\n'
                              f'Если кнопок нет, нажмите кнопку', reply_markup=skip)
    await state.update_data(photo=message.text)
    await state.update_data(file_id='</>')
    await state.set_state(new_card.add_buttons)

@cut.message(new_card.upload_photo)
async def add_upload(message: Message, state: FSMContext):
    await message.answer(text=f'Отправьте материалы для кнопок:\n'
                              f'Пример сообщения: Ссылка_на_материал текст_кнопки\n'
                              f'<b>Между ссылкой и текстом кнопки должен быть |</b>\n'
                              f'Если кнопок нет, нажмите кнопку', reply_markup=skip)
    data = message.photo[-1].file_id
    await state.update_data(file_id=data)
    await state.update_data(photo='</>')
    await state.set_state(new_card.add_buttons)

@cut.message(new_card.add_buttons)
async def finish_card(message: Message, state: FSMContext, bot: Bot):
    context_data = await state.get_data()
    name = context_data.get('name')
    description = context_data.get('description')
    photo = context_data.get('photo')
    file_id = context_data.get('file_id')
    await state.update_data(button=message.text)
    button = [str(x) for x in message.text.split('|')]
    builder = InlineKeyboardBuilder()
    caption = f'{name}\n{description}'
    if button[0] !='Нет':
        if photo != '</>':
            while len(button) > 0:
                builder.button(text=button[1], url=button[0])
                button[0], button[1] = '^^^^', '^^^^'
                button = [str(x) for x in button if x!='^^^^']
            builder.adjust(1)
            await bot.send_photo(photo=photo, caption=caption, reply_markup=builder.as_markup(), chat_id=message.from_user.id)
            await message.answer(text='<b>Создаем карточку?</b>\nДля изменения карточки на интересующий элемент.', reply_markup=confirm)
        else:
            while len(button) > 0:
                builder.button(text=button[1], url=button[0])
                button[0], button[1] = '^^^^', '^^^^'
                button = [str(x) for x in button if x!='^^^^']
            builder.adjust(1)
            await bot.send_photo(photo=file_id, caption=caption, reply_markup=builder.as_markup(), chat_id=message.from_user.id)
            await message.answer(text='<b>Создаем карточку?</b>\nДля изменения карточки на интересующий элемент.', reply_markup=confirm)
    else:
        if photo!='</>':
            await bot.send_photo(photo=photo, caption=caption, chat_id=message.from_user.id)
            await message.answer(text='<b>Создаем карточку?</b>\nДля изменения карточки на интересующий элемент.', reply_markup=confirm)
        else:
            await bot.send_photo(photo=file_id, caption=caption, chat_id=message.from_user.id)
            await message.answer(text='<b>Создаем карточку?</b>\nДля изменения карточки на интересующий элемент.', reply_markup=confirm)
    await state.set_state(new_card.finish_card)

@cut.callback_query(new_card.finish_card, F.data == "good_job")
async def good_job(call: CallbackQuery, state: FSMContext, bot: Bot):
    if (int(call.from_user.id) == superuser and list(*db.get_lang(call.from_user.id))[0] == 'RU') or \
            (str(call.from_user.id) in [str(db.get_admin_id_menu()[x][0]) for x in range(len(db.get_admin_id_menu()))] and list(*db.get_lang(call.from_user.id))[0] == 'RU'):
        context_data = await state.get_data()
        name = context_data.get('name')
        description = context_data.get('description')
        photo = context_data.get('photo')
        label = context_data.get('label')
        nxt = context_data.get('next')
        if nxt == '$ None':
            nxt = 'Конец'
        file_id = context_data.get('file_id')
        uin = context_data.get('uin')
        button = context_data.get('button').split('|')
        id = db.get_topic(label)[0][0]
        new_add = context_data.get('new_add')
        un = context_data.get('un')
        if len(button) == 1:
            link = text_link = 'Нет'
        else:
            link = ' '.join([button[x] for x in range(len(button)) if x%2==0])
            text_link = '|'.join([button[x] for x in range(len(button)) if x%2!=0])
        db.change_2(f'$ {uin}', nxt[2:])
        db.change_1(f'$ {uin}', un)
        if photo != '</>':
            if new_add == '1':
                db.add_card(id=id, uin=uin, label=label, name=name, description=description, previous="Начало",
                            next="Конец", photo=photo, file_id='0', link=link, link_text=text_link)
            else:
                db.add_card(id=id, uin=uin, label=label, name=name, description=description, previous='$' + ' ' + str(un),
                            next=nxt, photo=photo, file_id='0', link=link, link_text=text_link)
        else:
            if new_add == '1':
                db.add_card(id=id, uin=uin, label=label, name=name, description=description, previous="Начало",
                            next="Конец", file_id=file_id, photo='0', link=link, link_text=text_link)
            else:
                db.add_card(id=id, uin=uin, label=label, name=name, description=description, previous='$' + ' ' + str(un),
                            next=nxt, file_id=file_id, photo='0', link=link, link_text=text_link)

        await bot.send_message(chat_id=call.from_user.id, text='Карточка добавлена!', reply_markup=keyboard)
        db.commit()
        await call.answer()
        await state.clear()

@cut.callback_query(new_card.finish_card, F.data == "name_change")
async def name_change(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text=f'Отправьте измененное название:', chat_id=call.from_user.id)
    await state.update_data(change = 'name')
    await state.set_state(new_card.changed)
    await call.answer()

@cut.callback_query(new_card.finish_card, F.data == "description_change")
async def description_change(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text=f'Отправьте измененное описание:', chat_id=call.from_user.id)
    await state.update_data(change = 'description')
    await state.set_state(new_card.changed)
    await call.answer()

@cut.callback_query(new_card.finish_card, F.data == "photo_change")
async def photo_change(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text=f'Как вы хотите загруить фотографию?', reply_markup=photo, chat_id=call.from_user.id)
    await state.set_state(new_card.photo_change)
    await call.answer()

@cut.callback_query(new_card.finish_card, F.data == "button_change")
async def button_change(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text=f'Отправьте измененные кнопки:'
                                f'\n Пример сообщения: Ссылка_на_материал текст_кнопки'
                                f'\n<b>Между ссылкой и текстом кнопки должен быть |</b>'
                                f'\nЕсли кнопок нет, нажмите кнопку', reply_markup=skip, chat_id=call.from_user.id)
    await state.update_data(change = 'button')
    await state.set_state(new_card.changed)
    await call.answer()

@cut.callback_query(new_card.photo_change, F.data == "photo_link")
async def photo_link(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text=f'Отправьте ссылку на фотографию:', chat_id=call.from_user.id)
    await state.update_data(change = 'photo')
    await state.update_data(file_id = '</>')
    await state.set_state(new_card.changed)
    await call.answer()

@cut.callback_query(new_card.photo_change, F.data == "upload_photo")
async def upload_photo(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text=f'Отправьте фотографию:', chat_id=call.from_user.id)
    await state.update_data(change = 'file_id')
    await state.update_data(photo = '</>')
    await state.set_state(new_card.changed)
    await call.answer()


@cut.message(new_card.changed)
async def changed_card(message: Message, state: FSMContext, bot: Bot):
    context_data = await state.get_data()
    change = context_data.get('change')
    if change == 'button':
        button = [str(x) for x in message.text.split('|')]
        await state.update_data(button=message.text)
        file_id = context_data.get('file_id')
        name = context_data.get('name')
        description = context_data.get('description')
        photo = context_data.get('photo')
    elif change == 'name':
        name = message.text
        await state.update_data(name = name)
        description = context_data.get('description')
        photo = context_data.get('photo')
        button = [str(x) for x in context_data.get('button').split('|')]
        file_id = context_data.get('file_id')
    elif change == 'description':
        description = message.text
        await state.update_data(description=description)
        name = context_data.get('name')
        photo = context_data.get('photo')
        button = [str(x) for x in context_data.get('button').split('|')]
        file_id = context_data.get('file_id')
    elif change == 'file_id':
        file_id = message.photo[-1].file_id
        await state.update_data(file_id=file_id)
        description = context_data.get('description')
        name = context_data.get('name')
        photo = context_data.get('photo')
        button = [str(x) for x in context_data.get('button').split('|')]
    else:
        photo = message.text
        await state.update_data(photo=photo)
        description = context_data.get('description')
        name = context_data.get('name')
        button = [str(x) for x in context_data.get('button').split('|')]
        file_id = context_data.get('file_id')
    builder = InlineKeyboardBuilder()
    caption = f'{name}\n{description}'
    if button[0] != 'Нет':
        if photo != '</>':
            while len(button) > 0:
                builder.button(text=button[1], url=button[0])
                button[0], button[1] = '^^^^', '^^^^'
                button = [str(x) for x in button if x != '^^^^']
            builder.adjust(1)
            await bot.send_photo(photo=photo, caption=caption, reply_markup=builder.as_markup(),
                                 chat_id=message.from_user.id)
            await message.answer(text='<b>Создаем карточку?</b>\nДля изменения карточки на интересующий элемент.',
                                 reply_markup=confirm)
        else:
            while len(button) > 0:
                builder.button(text=button[1], url=button[0])
                button[0], button[1] = '^^^^', '^^^^'
                button = [str(x) for x in button if x != '^^^^']
            builder.adjust(1)
            await bot.send_photo(photo=file_id, caption=caption, reply_markup=builder.as_markup(),
                                 chat_id=message.from_user.id)
            await message.answer(text='<b>Создаем карточку?</b>\nДля изменения карточки на интересующий элемент.',
                                 reply_markup=confirm)
    else:
        if photo != '</>':
            await bot.send_photo(photo=photo, caption=caption, chat_id=message.from_user.id)
            await message.answer(text='<b>Создаем карточку?</b>\nДля изменения карточки на интересующий элемент.',
                                 reply_markup=confirm)
        else:
            await bot.send_photo(photo=file_id, caption=caption, chat_id=message.from_user.id)
            await message.answer(text='<b>Создаем карточку?</b>\nДля изменения карточки на интересующий элемент.',
                                 reply_markup=confirm)
    await state.set_state(new_card.finish_card)

