from aiogram import Router, F
from aiogram.types import Message
from database import Database
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from reply_keyboard import change_section, keyboard
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext
from inline_keyboard import deactivate
from aiogram.filters.command import Command

db = Database('db.db')
sect = Router()

class new_header(StatesGroup):
    get_header = State()
    get_group = State()
    delete_header = State()

@sect.message(Command('change_section'))
async def about(message: Message):
    if str(message.from_user.id) in [str(db.get_admin_id_menu()[x][0]) for x in range(len(db.get_admin_id_menu()))]:
        await message.answer(text = 'Что будем изменять в разделах?', reply_markup=change_section)

@sect.message(F.text == 'Добавить новый раздел')
async def new_layer(message: Message, state: FSMContext):
    if str(message.from_user.id) in [str(db.get_admin_id_menu()[x][0]) for x in range(len(db.get_admin_id_menu()))]:
        await message.answer(text='Напишите название новoго раздела', reply_markup=deactivate)
        await state.set_state(new_header.get_group)

@sect.message(new_header.get_group)
async def new_layer_1(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    await state.update_data(name=message.text)
    builder.button(text='- Художественная резка')
    builder.button(text='- Техническая резка')
    builder.button(text='- Выбрать аксессуары')
    builder.button(text='- Стайрофоминг-проект')
    builder.button(text='- Мастер-класс')
    builder.button(text='- Онлайн-курс')
    builder.button(text='- Выбрать расходные материалы')
    builder.adjust(1)
    await message.answer(text='В какую группу добавляем?', reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(new_header.get_header)

@sect.message(new_header.get_header)
async def finish_layer(message: Message, state: FSMContext):
    context_data = await state.get_data()
    topic = context_data.get('name')
    db.add_topic(topic, message.text[2:])
    await message.answer(text=f'Новый раздел добавлен!', reply_markup=keyboard)
    db.commit()
    await state.clear()

@sect.message(F.text == 'Удалить раздел')
async def delete_layer(message: Message, state: FSMContext):
    if str(message.from_user.id) in [str(db.get_admin_id_menu()[x][0]) for x in range(len(db.get_admin_id_menu()))]:
        builder = ReplyKeyboardBuilder()
        a = [x[0] for x in db.all_topic()]
        for i in a:
            builder.button(text='×' + ' ' + str(i))
        builder.adjust(1)
        await message.answer(text='Что будем удалять?', reply_markup=builder.as_markup(resize_keyboard=True))
        await message.answer(text = 'Нажмите на кнопку для отмены', reply_markup=deactivate)
        await state.set_state(new_header.delete_header)

@sect.message(F.text.startswith('×'), new_header.delete_header)
async def delete_layer_1(message: Message, state: FSMContext):
    header = message.text[2:]
    db.delete_headers(header)
    await message.answer(text=f'Раздел {header} удален!', reply_markup=keyboard)
    await state.clear()