from aiogram import Router, F, Bot
from aiogram.types import Message, InputMediaPhoto, CallbackQuery
from database import Database
from config import superuser
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from reply_keyboard import skip, keyboard
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext
from inline_keyboard import confirm_gallery, photo, gallery_delete, like_keyboard, admin_keyboard, update_gallery, deactivate

db = Database('db.db')
gal = Router()

class new_card(StatesGroup):
    add_gallery_name = State()
    add_gallery_photo = State()
    photo_gallery_link = State()
    upload_gallery_photo = State()
    add_gallery_buttons = State()
    finish_gallery_card = State()
    gallery_changed = State()
    photo_gallery_change = State()

class del_card(StatesGroup):
    conf_del = State()

class update_gallery_card(StatesGroup):
    update_gallery = State()
    finish_gallery_update = State()


@gal.message(F.text.in_({'Галерея работ', 'Gallery'}))
async def gallery(message: Message, bot: Bot, state: FSMContext):
    db.add_statistics(message.from_user.id, message.text, str(message.date)[:-15], str(message.date)[-14:-6])
    db.commit()
    inform = db.gallery_name()

    if len(inform) == 0:
        await message.answer(text = 'Похоже, в этом разделе нет карточек. Давайте ее создадим!\n'
                                    'Напишите название:')
        uinn = db.gallery_uin()
        uin_list = [int(uinn[x][0]) for x in range(len(list(db.gallery_uin())))]
        for i in range(100, 1000):
            if i not in uin_list:
                await state.update_data(uin=i)
                break
        await state.update_data(previous='Начало')
        await state.update_data(next='Конец')
        await state.update_data(new_add='1')
        await state.set_state(new_card.add_gallery_name)
    else:
        uin, name, likes, prv, nxt, photo, file_id, link, text_link = list(*inform)
        like = [x for x in str(*db.gallery_get_uin(uin)[0]).split() if x != 'None']
        builder = InlineKeyboardBuilder()
        link = str(link).split()
        text_link = str(text_link).split('|')
        builder.button(text='⬅', callback_data=f'G {str(list(*db.gallery_end())[0])}')
        like_keyboard(likes, message.from_user.id, uin, builder, len(like))
        if (prv == 'Начало') and (nxt == 'Конец'):
            pass
        else:
            builder.button(text='️➡', callback_data=nxt)
        builder.adjust(3)
        builder_button = InlineKeyboardBuilder()
        if link[0] != 'Нет':
            for i in range(len(link)):
                builder_button.button(text=text_link[i], url=link[i])
            builder_button.adjust(1)
        builder.attach(builder_button)
        if (int(message.from_user.id) == superuser and list(*db.get_lang(message.from_user.id))[0] == 'RU') or \
                (str(message.from_user.id) in [str(db.get_admin_id_gall()[x][0]) for x in range(len(db.get_admin_id_gall()))] and list(*db.get_lang(message.from_user.id))[0] == 'RU'):
            page = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Добавить следующую карту", callback_data=f'gnc{uin}'),
                    ],
                    [
                        InlineKeyboardButton(text="Изменить текущую карту", callback_data=f'glch{uin}'),
                    ],
                ],
            )
            builder.attach(InlineKeyboardBuilder.from_markup(page))
        if photo!= '0':

            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=photo,
                                 reply_markup=builder.as_markup())
        else:
            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=file_id,
                                 reply_markup=builder.as_markup())
    db.commit()

@gal.callback_query(F.data.startswith('like'))
async def likes(call: CallbackQuery, bot: Bot):
    uin = call.data[-3:]
    like = [x for x in str(*db.gallery_get_uin(uin)[0]).split() if x != 'None']
    if str(call.from_user.id) not in like:
        like.append(str(call.from_user.id))
    else:
        like.remove(str(call.from_user.id))
    db.gallery_add_like(' '.join(like), uin)
    uin, name, likes, prv, nxt, photo, file_id, link, text_link = list(*db.gallery_call_name(uin))
    builder = InlineKeyboardBuilder()
    link = str(link).split()
    text_link = str(text_link).split('|')
    if nxt == 'Конец':
        builder.button(text='⬅', callback_data=prv)
        like_keyboard(likes, call.from_user.id, uin, builder, len(like))
        builder.button(text='➡', callback_data=f'G {str(list(*db.gallery_start())[0])}')
        builder.adjust(3)
    elif prv == 'Начало':
        builder.button(text='⬅', callback_data=f'G {str(list(*db.gallery_end())[0])}')
        like_keyboard(likes, call.from_user.id, uin, builder, len(like))
        builder.button(text='️➡', callback_data=nxt)
        builder.adjust(3)
    else:
        builder.button(text='⬅', callback_data=prv)
        like_keyboard(likes, call.from_user.id, uin, builder, len(like))
        builder.button(text='️➡', callback_data=nxt)
        builder.adjust(3)
    builder_button = InlineKeyboardBuilder()
    if link[0] != 'Нет':
        for i in range(len(link)):
            builder_button.button(text=text_link[i], url=link[i])
        builder_button.adjust(1)
    builder.attach(builder_button)
    if (int(call.from_user.id) == superuser and list(*db.get_lang(call.from_user.id))[0] == 'RU') or \
            (str(call.from_user.id) in [str(db.get_admin_id_gall()[x][0]) for x in range(len(db.get_admin_id_gall()))] and list(*db.get_lang(call.from_user.id))[0] == 'RU'):
        admin_keyboard(prv, nxt, uin, builder)
    if photo != '0':
        await bot.edit_message_media(media=InputMediaPhoto(
            media=photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id, reply_markup=builder.as_markup())
    else:
        await bot.edit_message_media(media=InputMediaPhoto(
            media=file_id),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id, reply_markup=builder.as_markup())
    await call.answer()
    db.commit()

@gal.callback_query(F.data.startswith('glch'))
async def gallery_update_card(call: CallbackQuery, state: FSMContext, bot: Bot):
    if (int(call.from_user.id) == superuser and list(*db.get_lang(call.from_user.id))[0] == 'RU') or \
            (str(call.from_user.id) in [str(db.get_admin_id_gall()[x][0]) for x in range(len(db.get_admin_id_gall()))] and list(*db.get_lang(call.from_user.id))[0] == 'RU'):
        uin = call.data[-3:]
        await bot.send_message(chat_id=call.from_user.id, text = 'Что будем изменять?', reply_markup=update_gallery)
        await bot.send_message(text = 'Нажмите на кнопку для отмены', reply_markup=deactivate, chat_id=call.from_user.id)
        await state.update_data(uin = uin)
        await state.set_state(update_gallery_card.update_gallery)
    await call.answer()

@gal.callback_query(update_gallery_card.update_gallery, F.data == "name_change")
async def name_change(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text = 'Отправьте новое название:', chat_id=call.from_user.id)
    await call.answer()
    await state.update_data(change = 'name')
    await state.set_state(update_gallery_card.finish_gallery_update)

@gal.callback_query(update_gallery_card.update_gallery, F.data == "photo_change")
async def photo_change(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text = 'Отправьте новую фотографию:\n'
                                  '(Это может быть как файл, так и ссылка)', chat_id=call.from_user.id)
    await call.answer()
    await state.update_data(change = 'photo')
    await state.set_state(update_gallery_card.finish_gallery_update)

@gal.callback_query(update_gallery_card.update_gallery, F.data == "button_change")
async def button_change(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text = f'Отправьте измененные кнопки:'
                                f'\nПример сообщения: Ссылка_на_материал текст_кнопки'
                                f'\nМежду ссылкой и текстом кнопки должен быть |'
                                f'\nЕсли кнопок нет, нажмите кнопку', chat_id=call.from_user.id, reply_markup=skip)
    await call.answer()
    await state.update_data(change = 'button')
    await state.set_state(update_gallery_card.finish_gallery_update)

@gal.message(update_gallery_card.finish_gallery_update)
async def final_update(message: Message, state: FSMContext):
    if (int(message.from_user.id) == superuser and list(*db.get_lang(message.from_user.id))[0] == 'RU') or \
            (str(message.from_user.id) in [str(db.get_admin_id_gall()[x][0]) for x in range(len(db.get_admin_id_gall()))] and list(*db.get_lang(message.from_user.id))[0] == 'RU'):
        context_data = await state.get_data()
        change = context_data.get('change')
        uin = context_data.get('uin')
        if change == 'name':
            db.gallery_update_name(message.text, uin)
            await message.answer(text = 'Название изменено успешно!')
        elif change == 'photo':
            if message.photo:
                db.gallery_update_file_id(message.photo[-1].file_id, uin)
            else:
                db.gallery_update_photo(message.text, uin)
            await message.answer(text = 'Фотографя изменена успешно!')
        elif change == 'button':
            button = message.text.split('|')
            if len(button) == 1:
                link = text_link = 'Нет'
            else:
                link = ' '.join([button[x] for x in range(len(button)) if x % 2 == 0])
                text_link = '|'.join([button[x] for x in range(len(button)) if x % 2 != 0])
            db.gallery_update_buttons(link, text_link, uin)
        db.commit()
        await state.clear()

@gal.callback_query(F.data.startswith('G'))
async def call_gallery(call: CallbackQuery, bot: Bot):
    key = call.data[2:].strip()
    inform = db.gallery_call_name(key)
    uin, name, likes, prv, nxt, photo, file_id, link, text_link = list(*inform)
    link = str(link).split()
    text_link = str(text_link).split('|')
    like = [x for x in str(*db.gallery_get_uin(uin)[0]).split() if x != 'None']
    builder = InlineKeyboardBuilder()
    if nxt == 'Конец':
        builder.button(text='⬅', callback_data=prv)
        like_keyboard(likes, call.from_user.id, uin, builder, len(like))
        builder.button(text='➡', callback_data=f'G {str(list(*db.gallery_start())[0])}')
        builder.adjust(3)
    elif prv == 'Начало':
        builder.button(text='⬅', callback_data=f'G {str(list(*db.gallery_end())[0])}')
        like_keyboard(likes, call.from_user.id, uin, builder, len(like))
        builder.button(text='️➡', callback_data=nxt)
        builder.adjust(3)
    else:
        builder.button(text='⬅', callback_data=prv)
        like_keyboard(likes, call.from_user.id, uin, builder, len(like))
        builder.button(text='️➡', callback_data=nxt)
        builder.adjust(3)
    builder_button = InlineKeyboardBuilder()
    if link[0] != 'Нет':
        for i in range(len(link)):
            builder_button.button(text=text_link[i], url=link[i])
        builder_button.adjust(1)
    builder.attach(builder_button)
    if (int(call.from_user.id) == superuser and list(*db.get_lang(call.from_user.id))[0] == 'RU') or \
            (str(call.from_user.id) in [str(db.get_admin_id_gall()[x][0]) for x in range(len(db.get_admin_id_gall()))] and list(*db.get_lang(call.from_user.id))[0] == 'RU'):
        admin_keyboard(prv, nxt, uin, builder)
    if photo != '0':
        await bot.edit_message_media(media=InputMediaPhoto(
            media=photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id, reply_markup=builder.as_markup())
    else:
        await bot.edit_message_media(media=InputMediaPhoto(
            media=file_id),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id, reply_markup=builder.as_markup())
    await call.answer()



@gal.callback_query(F.data.startswith('gdl'))
async def delete_gallery_card(call: CallbackQuery, state: FSMContext, bot: Bot):
    if (int(call.from_user.id) == superuser and list(*db.get_lang(call.from_user.id))[0] == 'RU') or \
            (str(call.from_user.id) in [str(db.get_admin_id_gall()[x][0]) for x in range(len(db.get_admin_id_gall()))] and list(*db.get_lang(call.from_user.id))[0] == 'RU'):
        await state.update_data(prv = call.data[-5:])
        await state.update_data(nxt = call.data[-10:-5])
        await state.update_data(uin = call.data[-13:-10])
        await bot.send_message(chat_id=call.from_user.id, text = 'Вы точно хотите удалить карточку?', reply_markup= gallery_delete)
        await state.set_state(del_card.conf_del)
        await call.message.delete()
    await call.answer()

@gal.callback_query(del_card.conf_del, F.data == "gallery_del_1")
async def gallery_del_1(call: CallbackQuery, state: FSMContext, bot: Bot):
    if (int(call.from_user.id) == superuser and list(*db.get_lang(call.from_user.id))[0] == 'RU') or \
            (str(call.from_user.id) in [str(db.get_admin_id_gall()[x][0]) for x in range(len(db.get_admin_id_gall()))] and list(*db.get_lang(call.from_user.id))[0] == 'RU'):
        context_data = await state.get_data()
        prv = context_data.get('prv')
        nxt = context_data.get('nxt')
        uin = context_data.get('uin')
        db.gallery_delete_1(nxt, prv[2:])
        db.gallery_delete_2(prv, nxt[2:])
        db.gallery_delete(uin)
        db.commit()
        await state.clear()
        await call.message.delete()

@gal.callback_query(del_card.conf_del, F.data == "gallery_del_0")
async def gallery_del_0(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()

@gal.callback_query(F.data.startswith('gnc'))
async def add_name(call: CallbackQuery, state: FSMContext, bot: Bot):
    if (int(call.from_user.id) == superuser and list(*db.get_lang(call.from_user.id))[0] == 'RU') or \
            (str(call.from_user.id) in [str(db.get_admin_id_gall()[x][0]) for x in range(len(db.get_admin_id_gall()))] and list(*db.get_lang(call.from_user.id))[0] == 'RU'):
        await bot.send_message(text = 'Нажмите на кнопку для отмены', reply_markup=deactivate, chat_id=call.from_user.id)
        un =  call.data[-3:]
        await bot.send_message(text = 'Начинаем создание новой карточки \nНапишите название:', chat_id=call.from_user.id)
        await state.set_state(new_card.add_gallery_name)
        prv, nxt = list(*db.gallery_neighbours(un))
        await state.update_data(previous = prv)
        await state.update_data(next = nxt)
        await state.update_data(un = un)
        await state.update_data(new_add='0')
        uinn = db.gallery_uin()
        uin_list = [int(uinn[x][0]) for x in range(len(list(db.gallery_uin())))]
        for i in range(100, 1000):
            if i not in uin_list:
                await state.update_data(uin=i)
                break
        db.commit()
    await call.answer()

@gal.message(new_card.add_gallery_name)
async def add_photo(message: Message, state: FSMContext):
    await message.answer(text=f'Как вы хотите загруить фотографию?', reply_markup=photo)
    await state.update_data(name=message.text)
    await state.set_state(new_card.add_gallery_photo)

@gal.callback_query(new_card.add_gallery_photo, F.data == "photo_link")
async def gallery_link(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text=f'Отправьте ссылку на фото для карточки', chat_id=call.from_user.id)
    await state.set_state(new_card.photo_gallery_link)
    await call.answer()

@gal.callback_query(new_card.add_gallery_photo, F.data == "upload_photo")
async def upload_photo(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text=f'Отправьте фото для карточки', chat_id=call.from_user.id)
    await state.set_state(new_card.upload_gallery_photo)
    await call.answer()

@gal.message(new_card.photo_gallery_link)
async def buttons_gallery_1(message: Message, state: FSMContext):
    await message.answer(text=f'Отправьте материалы для кнопок:\n'
                              f'Пример сообщения: Ссылка_на_материал текст_кнопки\n'
                              f'<b>Между ссылкой и текстом кнопки должен быть |</b>\n'
                              f'Если кнопок нет, нажмите кнопку', reply_markup=skip)
    await state.update_data(photo=message.text)
    await state.update_data(file_id='</>')
    await state.set_state(new_card.add_gallery_buttons)

@gal.message(new_card.upload_gallery_photo)
async def buttons_gallery(message: Message, state: FSMContext):
    await message.answer(text=f'Отправьте материалы для кнопок:\n'
                              f'Пример сообщения: Ссылка_на_материал текст_кнопки\n'
                              f'<b>Между ссылкой и текстом кнопки должен быть |</b>\n'
                              f'Если кнопок нет, нажмите кнопку', reply_markup=skip)
    data = message.photo[-1].file_id
    await state.update_data(file_id=data)
    await state.update_data(photo='</>')
    await state.set_state(new_card.add_gallery_buttons)

@gal.message(new_card.add_gallery_buttons)
async def finish_card(message: Message, state: FSMContext, bot: Bot):
    context_data = await state.get_data()
    name = context_data.get('name')
    photo = context_data.get('photo')
    file_id = context_data.get('file_id')
    await state.update_data(button=message.text)
    button = [str(x) for x in message.text.split('|')]
    builder = InlineKeyboardBuilder()
    if button[0] !='Нет':
        if photo != '</>':
            while len(button) > 0:
                builder.button(text=button[1], url=button[0])
                button[0], button[1] = '^^^^', '^^^^'
                button = [str(x) for x in button if x!='^^^^']
            builder.adjust(1)
            await bot.send_photo(photo=photo, caption=name, reply_markup=builder.as_markup(), chat_id=message.from_user.id)
            await message.answer(text='<b>Создаем карточку?</b>\nДля изменения карточки на интересующий элемент.', reply_markup=confirm_gallery)
        else:
            while len(button) > 0:
                builder.button(text=button[1], url=button[0])
                button[0], button[1] = '^^^^', '^^^^'
                button = [str(x) for x in button if x!='^^^^']
            builder.adjust(1)
            await bot.send_photo(photo=file_id, caption=name, reply_markup=builder.as_markup(), chat_id=message.from_user.id)
            await message.answer(text='<b>Создаем карточку?</b>\nДля изменения карточки на интересующий элемент.', reply_markup=confirm_gallery)
    else:
        if photo!='</>':
            await bot.send_photo(photo=photo, caption=name, chat_id=message.from_user.id)
            await message.answer(text='<b>Создаем карточку?</b>\nДля изменения карточки на интересующий элемент.', reply_markup=confirm_gallery)
        else:
            await bot.send_photo(photo=file_id, caption=name, chat_id=message.from_user.id)
            await message.answer(text='<b>Создаем карточку?</b>\nДля изменения карточки на интересующий элемент.', reply_markup=confirm_gallery)
    await state.set_state(new_card.finish_gallery_card)

@gal.callback_query(new_card.finish_gallery_card, F.data == "good_job")
async def good_job(call: CallbackQuery, state: FSMContext, bot: Bot):
    if (int(call.from_user.id) == superuser and list(*db.get_lang(call.from_user.id))[0] == 'RU') or \
            (str(call.from_user.id) in [str(db.get_admin_id_gall()[x][0]) for x in range(len(db.get_admin_id_gall()))] and list(*db.get_lang(call.from_user.id))[0] == 'RU'):
        context_data = await state.get_data()
        name = context_data.get('name')
        photo = context_data.get('photo')
        nxt = context_data.get('next')
        if nxt == 'G None':
            nxt = 'Конец'
        file_id = context_data.get('file_id')
        uin = context_data.get('uin')
        button = context_data.get('button').split('|')
        new_add = context_data.get('new_add')
        un = context_data.get('un')
        if len(button) == 1:
            link = text_link = 'Нет'
        else:
            link = ' '.join([button[x] for x in range(len(button)) if x%2==0])
            text_link = '|'.join([button[x] for x in range(len(button)) if x%2!=0])
        db.gallery_change_2(f'G {uin}', nxt[2:])
        db.gallery_change_1(f'G {uin}', un)
        if photo != '</>':
            if new_add == '1':
                db.add_gallery_card(uin=uin, name=name, previous="Начало",
                            next="Конец", photo=photo, file_id='0', link=link, link_text=text_link)
            else:
                db.add_gallery_card(uin=uin, name=name, previous='G' + ' ' + str(un),
                            next=nxt, photo=photo, file_id='0', link=link, link_text=text_link)
        else:
            if new_add == '1':
                db.add_gallery_card(uin=uin, name=name, previous="Начало",
                            next="Конец", file_id=file_id, photo='0', link=link, link_text=text_link)
            else:
                db.add_gallery_card(uin=uin, name=name, previous='G' + ' ' + str(un),
                            next=nxt, file_id=file_id, photo='0', link=link, link_text=text_link)
        await bot.send_message(chat_id=call.from_user.id, text='Поздравляю! Работа добавлена в галерею!', reply_markup=keyboard)
        db.commit()
        await call.answer()
        await state.clear()

@gal.callback_query(new_card.finish_gallery_card, F.data == "name_change")
async def gallery_name_change(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text=f'Отправьте измененное название:', chat_id=call.from_user.id)
    await state.update_data(change = 'name')
    await state.set_state(new_card.gallery_changed)
    await call.answer()

@gal.callback_query(new_card.finish_gallery_card, F.data == "photo_change")
async def start_photo_change(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text=f'Как вы хотите загруить фотографию?', reply_markup=photo, chat_id=call.from_user.id)
    await state.set_state(new_card.photo_gallery_change)
    await call.answer()

@gal.callback_query(new_card.finish_gallery_card, F.data == "button_change")
async def gallery_button_change(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text=f'Отправьте измененные кнопки:'
                                f'\n Пример сообщения: Ссылка_на_материал текст_кнопки'
                                f'\n<b>Между ссылкой и текстом кнопки должен быть |</b>'
                                f'\nЕсли кнопок нет, нажмите кнопку', reply_markup=skip, chat_id=call.from_user.id)
    await state.update_data(change = 'button')
    await state.set_state(new_card.gallery_changed)
    await call.answer()

@gal.callback_query(new_card.photo_gallery_change, F.data == "photo_link")
async def gallery_photo_link(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text=f'Отправьте ссылку на фотографию:', chat_id=call.from_user.id)
    await state.update_data(change = 'photo')
    await state.update_data(file_id = '</>')
    await state.set_state(new_card.gallery_changed)
    await call.answer()

@gal.callback_query(new_card.photo_gallery_change, F.data == "upload_photo")
async def gallery_upload_photo(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(text=f'Отправьте фотографию:', chat_id=call.from_user.id)
    await state.update_data(change = 'file_id')
    await state.update_data(photo = '</>')
    await state.set_state(new_card.gallery_changed)
    await call.answer()

@gal.message(new_card.gallery_changed)
async def change_gallery_card(message: Message, state: FSMContext, bot: Bot):
    context_data = await state.get_data()
    change = context_data.get('change')
    if change == 'button':
        button = [str(x) for x in message.text.split('|')]
        await state.update_data(button=message.text)
        file_id = context_data.get('file_id')
        name = context_data.get('name')
        photo = context_data.get('photo')
    elif change == 'name':
        name = message.text
        await state.update_data(name = name)
        photo = context_data.get('photo')
        button = [str(x) for x in context_data.get('button').split('|')]
        file_id = context_data.get('file_id')
    elif change == 'file_id':
        file_id = message.photo[-1].file_id
        await state.update_data(file_id=file_id)
        name = context_data.get('name')
        photo = context_data.get('photo')
        button = [str(x) for x in context_data.get('button').split('|')]
    else:
        photo = message.text
        await state.update_data(photo=photo)
        name = context_data.get('name')
        button = [str(x) for x in context_data.get('button').split('|')]
        file_id = context_data.get('file_id')
    builder = InlineKeyboardBuilder()
    if button[0] != 'Нет':
        if photo != '</>':
            while len(button) > 0:
                builder.button(text=button[1], url=button[0])
                button[0], button[1] = '^^^^', '^^^^'
                button = [str(x) for x in button if x != '^^^^']
            builder.adjust(1)
            await bot.send_photo(photo=photo, caption=name, reply_markup=builder.as_markup(),
                                 chat_id=message.from_user.id)
            await message.answer(text='<b>Создаем карточку?</b>\nДля изменения карточки на интересующий элемент.',
                                 reply_markup=confirm_gallery)
        else:
            while len(button) > 0:
                builder.button(text=button[1], url=button[0])
                button[0], button[1] = '^^^^', '^^^^'
                button = [str(x) for x in button if x != '^^^^']
            builder.adjust(1)
            await bot.send_photo(photo=file_id, caption=name, reply_markup=builder.as_markup(),
                                 chat_id=message.from_user.id)
            await message.answer(text='<b>Создаем карточку?</b>\nДля изменения карточки на интересующий элемент.',
                                 reply_markup=confirm_gallery)
    else:
        if photo != '</>':
            await bot.send_photo(photo=photo, caption=name, chat_id=message.from_user.id)
            await message.answer(text='<b>Создаем карточку?</b>\nДля изменения карточки на интересующий элемент.',
                                 reply_markup=confirm_gallery)
        else:
            await bot.send_photo(photo=file_id, caption=name, chat_id=message.from_user.id)
            await message.answer(text='<b>Создаем карточку?</b>\nДля изменения карточки на интересующий элемент.',
                                 reply_markup=confirm_gallery)
    await state.set_state(new_card.finish_gallery_card)

