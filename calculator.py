from aiogram import Router, F, Bot
from aiogram.types import Message, InputMediaPhoto, CallbackQuery
from aiogram.utils.markdown import hlink
from database import Database
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext
from config import config
from reply_keyboard import percent, keyboard, keyboard_eng
from inline_keyboard import calculator, acrylic, deactivate, materials, materials_eng, calculator_choose_mat, deactivate_eng, acrylic_eng, calculator_eng
from telegraph import Telegraph



db = Database('db.db')
calc = Router()


class new_calculation(StatesGroup):
    stage = State()
    get_name = State()
    stage_1 = State() #Цена материала
    stage_1_acrylic = State() #Использованная краска
    stage_2_acrylic = State()
    stage_3_acrylic = State()
    stage_2 = State() #Использованный процент
    stage_3 = State() #Дополнительные материалы/Конец опроса
    stage_4 = State() #Дополнительные материалы
    stage_5 = State() #Дополнительные материалы
    stage_6 = State() #Конец опроса


@calc.message(F.text.in_({'Калькулятор расчета стоимости фигуры', 'Figure cost calculator'}))
async def calculator_start(message:Message, bot: Bot):
    db.add_statistics(message.from_user.id, message.text, str(message.date)[:-15], str(message.date)[-14:-6])
    db.commit()
    if not db.calc_exists(int(message.from_user.id)):
        db.add_calc(message.from_user.id)
    elif db.calc_exists(message.from_user.id):
        db.calc_update(message.from_user.id)
    db.commit()
    path = 'https://www.rezak-penoplasta-tvorec.ru/wp-content/uploads/2022/03/%D0%BC%D0%B8%D1%80-%D1%82%D0%B2%D0%BE%D1%80%D1%86%D0%B0.jpg'
    lang = list(*db.get_lang(message.from_user.id))[0]
    if lang == 'EN':
        await bot.send_photo(chat_id=message.from_user.id, photo=path, reply_markup=materials_eng, caption = "Congratulations on the job well done! Let's calculate its cost!")
    else:
        await bot.send_photo(chat_id=message.from_user.id, photo=path, reply_markup=materials, caption = 'Поздравляю с выполненной работой! Давай рассчитаем ее стоимость!')

@calc.callback_query(F.data.startswith('&'))
async def calc_call(call: CallbackQuery, bot: Bot):
    key = call.data[1:]
    user_id = call.from_user.id
    state = list(*db.calc_state(call.from_user.id))
    path = 'https://www.rezak-penoplasta-tvorec.ru/wp-content/uploads/2022/03/%D0%BC%D0%B8%D1%80-%D1%82%D0%B2%D0%BE%D1%80%D1%86%D0%B0.jpg'
    lang = list(*db.get_lang(call.from_user.id))[0]
    if key == 'styrofoam':
        if state[1] == '0':
            db.update_styrofoam('styrofoam', user_id)
        else:
            db.update_styrofoam('0', user_id)
    elif key == 'expanded':
        if state[2] == '0':
            db.update_expanded('expanded', user_id)
        else:
            db.update_expanded('0', user_id)
    elif key == 'roof':
        if state[3] == '0':
            db.update_roof('roof', user_id)
        else:
            db.update_roof('0', user_id)
    elif key == 'glue':
        if state[4] == '0':
            db.update_glue('glue', user_id)
        else:
            db.update_glue('0', user_id)
    elif key == 'priming':
        if state[5] == '0':
            db.update_priming('priming', user_id)
        else:
            db.update_priming('0', user_id)
    elif key == 'acrylic':
        if state[6] == '0':
            db.update_acrylic('acrylic', user_id)
        else:
            db.update_acrylic('0', user_id)
    elif key == 'varnish':
        if state[7] == '0':
            db.update_varnish('varnish', user_id)
        else:
            db.update_varnish('0', user_id)
    elif key == 'materials':
        if state[8] == '0':
            db.update_materials('materials', user_id)
        else:
            db.update_materials('0', user_id)
    new_state = list(*db.calc_state(call.from_user.id))
    if lang == 'RU':
        await bot.edit_message_media(media=InputMediaPhoto(
            media=path, caption = 'Поздравляю с выполненной работой! Давай рассчитаем ее стоимость!'), chat_id=call.message.chat.id,
            message_id=call.message.message_id, reply_markup=calculator_choose_mat(new_state, lang))
    else:
        await bot.edit_message_media(media=InputMediaPhoto(
            media=path, caption = "Congratulations on the job well done! Let's calculate its cost!"), chat_id=call.message.chat.id,
            message_id=call.message.message_id, reply_markup=calculator_choose_mat(new_state, lang))
    db.commit()
    await call.answer()

@calc.callback_query(F.data == 'save')
async def calculator_save_calc(call: CallbackQuery, bot: Bot, state: FSMContext):
    ls = [x for x in list(*(db.calc_state(call.from_user.id)))[1:-5] if x != '0']
    lang = list(*db.get_lang(call.from_user.id))[0]
    if len(ls) > 0:
        if lang == "RU":
            await bot.send_message(chat_id=call.from_user.id, text='Отправьте название работы')
            await bot.send_message(text='Нажмите на кнопку для отмены', reply_markup=deactivate, chat_id=call.from_user.id)
        else:
            await bot.send_message(chat_id=call.from_user.id, text='Send the title of the work')
            await bot.send_message(text='Press the button to cancel', reply_markup=deactivate_eng, chat_id=call.from_user.id)
        await state.set_state(new_calculation.get_name)
        await call.answer()
    else:
        if lang == "RU":
            await call.answer(text='Выберите используемые материалы')
        else:
            await call.answer(text='Choose the materials')

@calc.message(new_calculation.get_name)
async def calculator_save_calc(message:Message, bot: Bot, state: FSMContext):
    lst = [x for x in list(*(db.calc_state(message.from_user.id)))[1:-5] if x != '0'][0]
    await state.update_data(id=lst)
    await state.update_data(name = message.text)
    lang = list(*db.get_lang(message.from_user.id))[0]
    data = {'styrofoam': 'пенопласта', 'expanded': 'экструдированного пенеполистерола',
            'roof': 'потолочной плитки', 'glue': 'клея', 'priming': 'грунтовки',
            'acrylic': 'акриловой краски', 'varnish': 'лака', 'materials': 'остальных материалов'}
    data_eng = {'styrofoam': 'styrofoam', 'expanded': 'extruded polystyrene foam',
            'roof': 'ceiling tiles', 'glue': 'glue', 'priming': 'primer',
            'acrylic': 'acrylic paint', 'varnish': 'varnish', 'materials': 'other materials'}
    if lang == "RU":
        if lst == 'materials':
            await bot.send_message(chat_id=message.from_user.id, text=f'Напишите стоимость {data[lst]}',
                                   reply_markup=ReplyKeyboardRemove())
            await state.set_state(new_calculation.stage_2)
        elif lst == 'acrylic':
            await bot.send_message(chat_id=message.from_user.id, text=f'Сколько баночек краски вы использовали?\n'
                                                                   f'(Одна баночка - это один использованный в работе цвет)')
            await state.set_state(new_calculation.stage_1_acrylic)
        else:
            await bot.send_message(chat_id=message.from_user.id, text = f'Напишите стоимость {data[lst]}', reply_markup=ReplyKeyboardRemove())
            await state.set_state(new_calculation.stage_1)
    else:
        if lst == 'materials':
            await bot.send_message(chat_id=message.from_user.id, text=f'Write cost of the {data_eng[lst]}',
                                   reply_markup=ReplyKeyboardRemove())
            await state.set_state(new_calculation.stage_2)
        elif lst == 'acrylic':
            await bot.send_message(chat_id=message.from_user.id, text=f'How many jars of paint did you use?\n'
                                                                   f'(One jar is one color used in the work)')
            await state.set_state(new_calculation.stage_1_acrylic)
        else:
            await bot.send_message(chat_id=message.from_user.id, text = f'Write cost of the {data_eng[lst]}', reply_markup=ReplyKeyboardRemove())
            await state.set_state(new_calculation.stage_1)
    db.commit()


@calc.message(new_calculation.stage_1)
async def calculator_cost(message: Message, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(message.from_user.id))[0]
    try:
        num = float(str(message.text).replace(',', '.'))
        await state.update_data(cost=message.text)
        if lang == 'RU':
            await bot.send_message(chat_id=message.from_user.id,
                                   text = f'Сколько процентов материала вы использовали?', reply_markup=percent)
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text = f'How many percent of the material did you use?', reply_markup=percent)
        await state.set_state(new_calculation.stage_2)
    except:
        data = {'styrofoam': 'пенопласта', 'expanded': 'экструдированного пенеполистерола',
                'roof': 'потолочной плитки', 'glue': 'клея', 'priming': 'грунтовки',
                'acrylic': 'акриловой краски', 'varnish': 'лака', 'materials': 'остальных материалов'}
        data_eng = {'styrofoam': 'styrofoam', 'expanded': 'extruded polystyrene foam',
                    'roof': 'ceiling tiles', 'glue': 'glue', 'priming': 'primer',
                    'acrylic': 'acrylic paint', 'varnish': 'varnish', 'materials': 'other materials'}
        context_data = await state.get_data()
        id = context_data.get('id')
        if lang == 'RU':
            await bot.send_message(chat_id=message.from_user.id, text=f'Это не число!\n'
                                                                      f'Напишите стоимость {data[id]}',
                                   reply_markup=ReplyKeyboardRemove())
        else:
            await bot.send_message(chat_id=message.from_user.id, text=f"It's not a number\n"
                                                                      f"Write cost of the {data_eng[id]}",
                                   reply_markup=ReplyKeyboardRemove())
        await state.set_state(new_calculation.stage_1)

@calc.message(new_calculation.stage_1_acrylic)
async def cost_1(message: Message, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(message.from_user.id))[0]
    try:
        if int(message.text) != 0 and int(message.text) < 51:
            await state.update_data(acrylic_number=message.text)
            if lang == 'RU':
                await bot.send_message(chat_id=message.from_user.id, text='Каждая баночка стоит одинаково?',
                                   reply_markup=acrylic)
            else:
                await bot.send_message(chat_id=message.from_user.id, text='Does each jar cost the same?',
                                   reply_markup=acrylic_eng)
            await state.set_state(new_calculation.stage_2_acrylic)
        else:
            if lang == 'RU':
                await bot.send_message(chat_id=message.from_user.id, text=f'Нужно от 1 до 50 баночек.\n'
                                                                          f'Сколько баночек краски вы использовали?')
            else:
                await bot.send_message(chat_id=message.from_user.id, text=f'You need to use from 1 to 50 jars.')
            await state.set_state(new_calculation.stage_1_acrylic)
    except:
        if lang == 'RU':
            await bot.send_message(chat_id=message.from_user.id, text=f'Ошибка! Попробуйте снова!\n'
                                                                      f'Сколько баночек краски вы использовали?')
        else:
            await bot.send_message(chat_id=message.from_user.id, text=f'Mistake! Try again!')
        await state.set_state(new_calculation.stage_1_acrylic)



@calc.callback_query(new_calculation.stage_2_acrylic, F.data == 'acryl_1')
async def acryl_cost(call: CallbackQuery, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(call.from_user.id))[0]
    if lang == 'RU':
        await bot.send_message(chat_id=call.from_user.id, text='Введите цену краски:')
    else:
        await bot.send_message(chat_id=call.from_user.id, text='Enter the price of the paint:')
    await state.update_data(acrylic_multi=False)
    await state.set_state(new_calculation.stage_3_acrylic)
    await call.answer()

@calc.callback_query(new_calculation.stage_2_acrylic, F.data == 'acryl_0')
async def acryl_percent(call: CallbackQuery, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(call.from_user.id))[0]
    if lang == 'RU':
        await bot.send_message(chat_id=call.from_user.id, text='Введите через пробел сколько стоит каждая баночка краски:\n'
                                                               '<b>Пример: 320 450 150 150</b>')
    else:
        await bot.send_message(chat_id=call.from_user.id, text='Enter, separated by a space, how much each jar of paint costs:\n'
                                                               '<b>Example: 320 450 150 150</b>')
    await state.update_data(acrylic_multi=True)
    await state.set_state(new_calculation.stage_3_acrylic)
    await call.answer()

@calc.message(new_calculation.stage_3_acrylic)
async def finish_acryl(message: Message, state: FSMContext, bot: Bot):
    context_data = await state.get_data()
    acrylic_number = int(context_data.get('acrylic_number'))
    acrylic_multi = context_data.get('acrylic_multi')
    await state.update_data(cost=message.text)
    lang = list(*db.get_lang(message.from_user.id))[0]
    if acrylic_multi == True:
        if len(message.text.split()) == acrylic_number:
            if lang == 'RU':
                await bot.send_message(chat_id=message.from_user.id, text='Введите через пробел сколько процентов каждой краски вы использовали:\n'
                                                                  '<b>Пример: 15 25 45 12</b>')
            else:
                await bot.send_message(chat_id=message.from_user.id, text='Enter, separated by a space, how many percent of each paint you used:\n'
                                                                  '<b>Example: 15 25 45 12</b>')
            await state.set_state(new_calculation.stage_2)
        else:
            if lang == 'RU':
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Введите через пробел сколько стоит каждая баночка краски:\n'
                                            '<b>Пример: 320 450 150 150</b>')
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Enter, separated by a space, how much each jar of paint costs:\n'
                                            '<b>Example: 320 450 150 150</b>')
            await state.set_state(new_calculation.stage_3_acrylic)
    else:
        if lang == 'RU':
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Введите через пробел сколько процентов каждой краски вы использовали:\n'
                                        '<b>Пример: 15 25 45 12</b>')
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Enter, separated by a space, how many percent of each paint you used:\n'
                                        '<b>Example: 15 25 45 12</b>')
        await state.set_state(new_calculation.stage_2)


@calc.message(new_calculation.stage_2)
async def final_calc(message: Message, state: FSMContext, bot: Bot):
    context_data = await state.get_data()
    id = context_data.get('id')
    acrylic_cost = 0
    lang = list(*db.get_lang(message.from_user.id))[0]
    acrylic_number = context_data.get('acrylic_number') if context_data.get('acrylic_number')!=None else None
    if id == 'materials':
        cost = float(str(message.text).replace(',', '.'))
        percent = 0
    elif id == 'acrylic':
        if len(message.text.split()) == int(acrylic_number):
            acrylic_multi = context_data.get('acrylic_multi')
            if acrylic_multi == False:
                cost = float(str(context_data.get('cost')).replace(',', '.'))
                percent = sum([((int(x) * cost)/100) for x in message.text.split()])
                acrylic_cost = percent
            else:
                cost = [float(x) for x in str(context_data.get('cost')).replace(',', '.').split()]
                percent = [int(x) for x in message.text.split()]
                acrylic_cost = sum(((cost[x] * percent[x]) / 100) for x in range(len(cost)))
        else:
            if lang == 'RU':
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ввели неверное количество процентов.\n'
                                            'Введите через пробел сколько процентов каждой краски вы использовали:\n'
                                            '<b>Пример: 15 25 45 12</b>')
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Enter, separated by a space, how many percent of each paint you used:\n'
                                            '<b>Example: 15 25 45 12</b>')
            percent = 0
            cost = 0
            await state.set_state(new_calculation.stage_2)
    else:
        cost = float(str(context_data.get('cost')).replace(',', '.'))
        percent = message.text
    data = {'styrofoam': 'пенопласта', 'expanded': 'экструдированного пенеполистерола',
                'roof': 'потолочной плитки', 'glue': 'клея', 'priming': 'грунтовки',
                'acrylic': 'акриловой краски', 'varnish': 'лака', 'materials': 'остальных материалов'}
    data_eng = {'styrofoam': 'styrofoam', 'expanded': 'extruded polystyrene foam',
                'roof': 'ceiling tiles', 'glue': 'glue', 'priming': 'primer',
                'acrylic': 'acrylic paint', 'varnish': 'varnish', 'materials': 'other materials'}
    user_id = message.from_user.id
    text = 'Это не число! Введите снова.' if lang == 'RU' else "It's not a number! Enter it again."
    if id == 'styrofoam':
        try:
            db.update_styrofoam('0', user_id)
            db.update_warning('0', user_id)
            await state.update_data(styrofoam_cost=str(float((cost * float(percent))/100)))
        except:
            await message.answer(text=text)
            db.update_warning('1', user_id)
    elif id == 'expanded':
        try:
            db.update_expanded('0', user_id)
            db.update_warning('0', user_id)
            await state.update_data(expanded_cost=str(float((cost * float(percent))/100)))
        except:
            await message.answer(text=text)
            db.update_warning('1', user_id)
    elif id == 'roof':
        try:
            db.update_roof('0', user_id)
            db.update_warning('0', user_id)
            await state.update_data(roof_cost=str(float((cost * float(percent))/100)))
        except:
            await message.answer(text=text)
            db.update_warning('1', user_id)
    elif id == 'glue':
        try:
            db.update_glue('0', user_id)
            db.update_warning('0', user_id)
            await state.update_data(glue_cost=str(float((cost * float(percent))/100)))
        except:
            await message.answer(text=text)
            db.update_warning('1', user_id)
    elif id == 'priming':
        try:
            db.update_priming('0', user_id)
            db.update_warning('0', user_id)
            await state.update_data(priming_cost=str(float((cost * float(percent))/100)))
        except:
            await message.answer(text=text)
            db.update_warning('1', user_id)
    elif id == 'acrylic':
        try:
            db.update_acrylic('0', user_id)
            db.update_warning('0', user_id)
            await state.update_data(acrylic_cost=acrylic_cost)
        except:
            await message.answer(text=text)
            db.update_warning('1', user_id)
    elif id == 'varnish':
        try:
            db.update_varnish('0', user_id)
            db.update_warning('0', user_id)
            await state.update_data(varnish_cost=str(float((cost * float(percent))/100)))
        except:
            await message.answer(text=text)
            db.update_warning('1', user_id)
    elif id == 'materials':
        try:
            db.update_materials('0', user_id)
            db.update_warning('0', user_id)
            await state.update_data(materials_cost=cost)
        except:
            await message.answer(text=text)
            db.update_warning('1', user_id)
    lst = [x for x in list(*(db.calc_state(message.from_user.id)))[1:-5] if x != '0']
    if str(list(*db.get_warning(user_id))[0]) != '1':
        if len(lst) != 0:
            lst = [x for x in list(*(db.calc_state(message.from_user.id)))[1:-5] if x != '0'][0]
            await state.update_data(id=lst)
            if lang == 'RU':
                if lst == 'materials':
                    await bot.send_message(chat_id=message.from_user.id, text=f'Напишите стоимость {data[lst]}',
                                           reply_markup=ReplyKeyboardRemove())
                    await state.set_state(new_calculation.stage_2)
                elif lst == 'acrylic':
                    await bot.send_message(chat_id=message.from_user.id, text=f'Сколько баночек краски вы использовали?\n'
                                                                           f'(Одна баночка - это один использованный в работе цвет)')
                    await state.set_state(new_calculation.stage_1_acrylic)
                else:
                    await bot.send_message(chat_id=message.from_user.id, text=f'Напишите стоимость {data[lst]}',
                                           reply_markup=ReplyKeyboardRemove())
                    await state.set_state(new_calculation.stage_1)
            else:
                if lst == 'materials':
                    await bot.send_message(chat_id=message.from_user.id, text=f'Write cost of the {data_eng[lst]}',
                                           reply_markup=ReplyKeyboardRemove())
                    await state.set_state(new_calculation.stage_2)
                elif lst == 'acrylic':
                    await bot.send_message(chat_id=message.from_user.id, text=f'How many jars of paint did you use?\n'
                                                                              f'(One jar is one color used in the work)')
                    await state.set_state(new_calculation.stage_1_acrylic)
                else:
                    await bot.send_message(chat_id=message.from_user.id, text=f'Write cost of the {data_eng[lst]}',
                                           reply_markup=ReplyKeyboardRemove())
                    await state.set_state(new_calculation.stage_1)
        else:
            other_inf = list(*db.get_dop_calc(user_id))
            if lang == 'RU':
                dop_info = (f'Налог: {other_inf[0]}%\n'
                            f'Амортизация: {other_inf[1]}%\n'
                            f'Прибыль с работы: {other_inf[2]}%\n'
                            f'Стоимость работы: {other_inf[3]}₽\n')
                remember_info = f'Я запомнил материалы! Будем ли мы изменять дополнительные параметры?'
            else:
                dop_info = (f'Taxes: {other_inf[0]}%\n'
                            f'Amortization: {other_inf[1]}%\n'
                            f'Profit: {other_inf[2]}%\n'
                            f'The cost of the work: {other_inf[3]}₽\n')
                remember_info = f'I remember the materials! Will we change additional parameters?'
            if id != 'acrylic':
                await bot.send_message(chat_id=message.from_user.id,
                                       text=remember_info, reply_markup=ReplyKeyboardRemove())
                if lang == 'RU':
                    await bot.send_message(chat_id=message.from_user.id, text=dop_info, reply_markup=calculator)
                else:
                    await bot.send_message(chat_id=message.from_user.id, text=dop_info, reply_markup=calculator_eng)

                await state.set_state(new_calculation.stage_3)
            elif (id == 'acrylic') and (len(message.text.split()) == int(acrylic_number)):
                await bot.send_message(chat_id=message.from_user.id,
                                       text=remember_info, reply_markup=ReplyKeyboardRemove())
                if lang == 'RU':
                    await bot.send_message(chat_id=message.from_user.id, text=dop_info, reply_markup=calculator)
                else:
                    await bot.send_message(chat_id=message.from_user.id, text=dop_info, reply_markup=calculator_eng)
                await state.set_state(new_calculation.stage_3)
    else:
        await state.set_state(new_calculation.stage_2)

    db.commit()



@calc.callback_query(new_calculation.stage_3, F.data == "calc_tax")
async def taxes(call: CallbackQuery, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(call.from_user.id))[0]
    if lang == 'RU':
        await bot.send_message(text=f'Сколько процентов вы закладываете на налоги?', chat_id=call.from_user.id)
    else:
        await bot.send_message(text=f'How much of a percentage do you budget for taxes?', chat_id=call.from_user.id)
    await state.update_data(previous = call.data)
    await state.set_state(new_calculation.stage_4)
    await call.answer()

@calc.callback_query(new_calculation.stage_3, F.data == "calc_amortization")
async def amortization(call: CallbackQuery, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(call.from_user.id))[0]
    if lang == 'RU':
        await bot.send_message(text=f'Сколько процентов вы закладываете на амортизацию?', chat_id=call.from_user.id)
    else:
        await bot.send_message(text=f'How much of a percentage do you budget for amortization?', chat_id=call.from_user.id)
    await state.update_data(previous = call.data)
    await state.set_state(new_calculation.stage_4)
    await call.answer()

@calc.callback_query(new_calculation.stage_3, F.data == "calc_work")
async def work(call: CallbackQuery, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(call.from_user.id))[0]
    if lang == 'RU':
        await bot.send_message(text=f'Сколько стоит час вашей работы?', chat_id=call.from_user.id)
    else:
        await bot.send_message(text=f'How much does an hour of your work cost?', chat_id=call.from_user.id)

    await state.update_data(previous = call.data)
    await state.set_state(new_calculation.stage_4)
    await call.answer()

@calc.callback_query(new_calculation.stage_3, F.data == "calc_profit")
async def profit(call: CallbackQuery, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(call.from_user.id))[0]
    if lang == 'RU':
        await bot.send_message(text=f'Сколько процентов прибыли вы хотите получать?', chat_id=call.from_user.id)
    else:
        await bot.send_message(text=f'How much percentage of profit do you want to make?', chat_id=call.from_user.id)

    await state.update_data(previous = call.data)
    await state.set_state(new_calculation.stage_4)
    await call.answer()


@calc.message(new_calculation.stage_4)
async def dop_info(message: Message, state: FSMContext, bot: Bot):
    context_data = await state.get_data()
    previous = context_data.get('previous')
    lang = list(*db.get_lang(message.from_user.id))[0]
    if previous == "calc_tax":
        try:
            int(message.text)
            db.update_tax(message.text, message.from_user.id)
        except:
            if lang == 'RU':
                await bot.send_message(chat_id=message.from_user.id, text='Это не целое число! Изменения отменены.')
            else:
                await bot.send_message(chat_id=message.from_user.id, text='This is not an integer! The changes have been cancelled.')
    elif previous == "calc_amortization":
        try:
            int(message.text)
            db.update_amortization(message.text, message.from_user.id)
        except:
            if lang == 'RU':
                await bot.send_message(chat_id=message.from_user.id, text='Это не целое число! Изменения отменены.')
            else:
                await bot.send_message(chat_id=message.from_user.id, text='This is not an integer! The changes have been cancelled.')
    elif previous == "calc_work":
        try:
            int(message.text)
            db.update_work(message.text, message.from_user.id)
        except:
            if lang == 'RU':
                await bot.send_message(chat_id=message.from_user.id, text='Это не целое число! Изменения отменены.')
            else:
                await bot.send_message(chat_id=message.from_user.id, text='This is not an integer! The changes have been cancelled.')
    elif previous == "calc_profit":
        try:
            int(message.text)
            db.update_profit(message.text, message.from_user.id)
        except:
            if lang == 'RU':
                await bot.send_message(chat_id=message.from_user.id, text='Это не целое число! Изменения отменены.')
            else:
                await bot.send_message(chat_id=message.from_user.id, text='This is not an integer! The changes have been cancelled.')
    other_inf = list(*db.get_dop_calc(message.from_user.id))
    lang = list(*db.get_lang(message.from_user.id))[0]
    if lang == 'RU':
        dop_info = (f'Налог: {other_inf[0]}%\n'
                    f'Амортизация: {other_inf[1]}%\n'
                    f'Прибыль с работы: {other_inf[2]}%\n'
                    f'Стоимость работы: {other_inf[3]}₽\n')
    else:
        dop_info = (f'Taxes: {other_inf[0]}%\n'
                    f'Amortization: {other_inf[1]}%\n'
                    f'Profit: {other_inf[2]}%\n'
                    f'The cost of the work: {other_inf[3]}₽\n')
    if lang == 'RU':
        await bot.send_message(chat_id=message.from_user.id, text=dop_info, reply_markup=calculator)
    else:
        await bot.send_message(chat_id=message.from_user.id, text=dop_info, reply_markup=calculator_eng)
    await state.set_state(new_calculation.stage_3)
    db.commit()

@calc.callback_query(new_calculation.stage_3, F.data == "calc_hour")
async def hours(call: CallbackQuery, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(call.from_user.id))[0]
    if lang == 'RU':
        await bot.send_message(chat_id=call.from_user.id, text = 'Сколько часов вы делали эту работу?')
    else:
        await bot.send_message(chat_id=call.from_user.id, text = 'How many hours did you do this work?')
    await call.answer()
    await state.set_state(new_calculation.stage_5)

@calc.message(new_calculation.stage_6)
async def hours_1(message: Message, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(message.from_user.id))[0]
    if lang == 'RU':
        await bot.send_message(chat_id=message.from_user.id, text='Сколько часов вы делали эту работу?\n'
                                                                  'Округлите время до получаса')
    else:
        await bot.send_message(chat_id=message.from_user.id, text = 'How many hours did you do this work?\n'
                                                                    'Round the time up to half an hour')
    await state.set_state(new_calculation.stage_5)

@calc.message(new_calculation.stage_5)
async def finish(message: Message, state: FSMContext, bot: Bot):
    lang = list(*db.get_lang(message.from_user.id))[0]
    try:
        if float(str(message.text).replace(',', '.')) % 0.5 == 0:
            hours = float(message.text)
            data = {'styrofoam': 'Стоимость пенопласта', 'expanded': 'Стоимость экструдированного пенополистерола',
                    'roof': 'Стоимость потолочной плитки', 'glue': 'Стоимость клея', 'priming': 'Стоимость грунтовки',
                    'acrylic': 'Стоимость акриловой краски', 'varnish': 'Стоимость лака',
                    'materials': 'Стоимость остальных материалов'}
            data_eng = {'styrofoam': 'Styrofoam', 'expanded': 'Extruded polystyrene foam',
                        'roof': 'Ceiling tiles', 'glue': 'Glue', 'priming': 'Primer',
                        'acrylic': 'Acrylic paint', 'varnish': 'Varnish', 'materials': 'Other materials'}
            other_inf = list(*db.get_dop_calc(message.from_user.id))
            tax = int(other_inf[0])
            amortization = int(other_inf[1])
            profit = int(other_inf[2])
            work = int(other_inf[3])
            context_data = await state.get_data()
            name = context_data.get('name')
            styrofoam_cost = float(context_data.get('styrofoam_cost')) if context_data.get('styrofoam_cost') != None else 0
            expanded_cost = float(context_data.get('expanded_cost')) if context_data.get('expanded_cost') != None else 0
            roof_cost = float(context_data.get('roof_cost')) if context_data.get('roof_cost') != None else 0
            glue_cost = float(context_data.get('glue_cost')) if context_data.get('glue_cost') != None else 0
            priming_cost = float(context_data.get('priming_cost')) if context_data.get('priming_cost') != None else 0
            acrylic_cost = float(context_data.get('acrylic_cost')) if context_data.get('acrylic_cost') != None else 0
            varnish_cost = float(context_data.get('varnish_cost')) if context_data.get('varnish_cost') != None else 0
            materials_cost = float(context_data.get('materials_cost')) if context_data.get('materials_cost') != None else 0
            itog = f''
            html_itog = f''
            if styrofoam_cost != 0:
                itog += f'{data["styrofoam"]}: {round(styrofoam_cost)}\n' if lang == 'RU' else f'{data_eng["styrofoam"]}: {round(styrofoam_cost)}\n'
                html_itog += f'<li>{data["styrofoam"]}: {round(styrofoam_cost)}</li>' if lang == 'RU' else f'<li>{data_eng["styrofoam"]}: {round(styrofoam_cost)}</li>'
            if expanded_cost != 0:
                itog += f'{data["expanded"]}: {round(expanded_cost)}\n' if lang == 'RU' else f'{data_eng["expanded"]}: {round(expanded_cost)}\n'
                html_itog += f'<li>{data["expanded"]}: {round(expanded_cost)}</li>' if lang == 'RU' else f'<li>{data_eng["expanded"]}: {round(expanded_cost)}</li>'
            if roof_cost != 0:
                itog += f'{data["roof"]}: {round(roof_cost)}\n' if lang == 'RU' else f'{data_eng["roof"]}: {round(roof_cost)}\n'
                html_itog += f'<li>{data["roof"]}: {round(roof_cost)}</li>' if lang == 'RU' else f'<li>{data_eng["roof"]}: {round(roof_cost)}</li>'
            if glue_cost != 0:
                itog += f'{data["glue"]}: {round(glue_cost)}\n' if lang == 'RU' else f'{data_eng["glue"]}: {round(glue_cost)}\n'
                html_itog += f'<li>{data["glue"]}: {round(glue_cost)}</li>' if lang == 'RU' else f'<li>{data_eng["glue"]}: {round(glue_cost)}</li>'
            if priming_cost != 0:
                itog += f'{data["priming"]}: {round(priming_cost)}\n' if lang == 'RU' else f'{data_eng["priming"]}: {round(priming_cost)}\n'
                html_itog += f'<li>{data["priming"]}: {round(priming_cost)}</li>' if lang == 'RU' else f'<li>{data_eng["priming"]}: {round(priming_cost)}</li>'
            if acrylic_cost != 0:
                itog += f'{data["acrylic"]}: {round(acrylic_cost)}\n' if lang == 'RU' else f'{data_eng["acrylic"]}: {round(acrylic_cost)}\n'
                html_itog += f'<li>{data["acrylic"]}: {round(acrylic_cost)}</li>' if lang == 'RU' else f'<li>{data_eng["acrylic"]}: {round(acrylic_cost)}</li>'
            if varnish_cost != 0:
                itog += f'{data["varnish"]}: {round(varnish_cost)}\n' if lang == 'RU' else f'{data_eng["varnish"]}: {round(varnish_cost)}\n'
                html_itog += f'<li>{data["varnish"]}: {round(varnish_cost)}</li>' if lang == 'RU' else f'<li>{data_eng["varnish"]}: {round(varnish_cost)}</li>'
            if materials_cost != 0:
                itog += f'{data["materials"]}: {round(materials_cost)}\n' if lang == 'RU' else f'{data_eng["materials"]}: {round(materials_cost)}\n'
                html_itog += f'<li>{data["materials"]}: {round(materials_cost)}</li>' if lang == 'RU' else f'<li>{data_eng["materials"]}: {round(materials_cost)}</li>'
            summ = float(styrofoam_cost) + float(expanded_cost) + float(roof_cost) + float(glue_cost) + float(
                priming_cost) + float(acrylic_cost) + float(varnish_cost) + float(materials_cost)
            itog += (f'<b>Сумма всех материалов: {round(summ)}</b>\n') if lang == 'RU' else (f'<b>The amount of materials: {round(summ)}</b>\n')
            final = summ + ((tax * summ) / 100) + ((profit * summ) / 100) + ((amortization * summ) / 100) + (work * hours)
            itog += (f'<ins><b>Итоговая стоимость: {round(final)}</b></ins>\n') if lang == 'RU' else (f'<ins><b>Total cost: {round(final)}</b></ins>\n')
            if lang == 'RU':
                await bot.send_message(chat_id=message.from_user.id, text=itog, reply_markup=keyboard)
            else:
                await bot.send_message(chat_id=message.from_user.id, text=itog, reply_markup=keyboard_eng)
            path = str(list(*db.get_telegraph(user_id=message.from_user.id))[0][19:])
            if lang == 'RU':
                web_land = hlink('Страница с расчетами',
                                 f'{list(*db.get_telegraph(user_id=message.from_user.id))[0]}')
            else:
                web_land = hlink('Page with calculations',
                                 f'{list(*db.get_telegraph(user_id=message.from_user.id))[0]}')
            telegraph = Telegraph(config.telegraph_token.get_secret_value())
            if lang == 'RU':
                telegraph.edit_page(
                    path=path,
                    title=f"{message.from_user.first_name}, это страница со всеми расчетами",
                    html_content=f"{telegraph.get_page(path = path)['content']}"
                                 f"<h3>{name}</h3>"
                                 f"<ul>{html_itog}</ul>",
                    author_name="rezak_tvorec_bot",
                    author_url="https://t.me/rezak_tvorec_bot",
                    return_content=False)
            else:
                telegraph.edit_page(
                    path=path,
                    title=f"{message.from_user.first_name}, this is a page with all the calculations",
                    html_content=f"{telegraph.get_page(path = path)['content']}"
                                 f"<h3>{name}</h3>"
                                 f"<ul>{html_itog}</ul>",
                    author_name="rezak_tvorec_bot",
                    author_url="https://t.me/rezak_tvorec_bot",
                    return_content=False)
            await bot.send_message(chat_id=message.from_user.id, text=web_land)
            await state.clear()
        else:
            if lang == 'RU':
                await bot.send_message(chat_id=message.from_user.id, text='Сколько часов вы делали эту работу?\n'
                                                                          'Округлите время до получаса')
            else:
                await bot.send_message(chat_id=message.from_user.id, text='How many hours did you do this work?\n'
                                                                          'Round the time up to half an hour')
            await state.set_state(new_calculation.stage_6)
    except:
        if lang == 'RU':
            await bot.send_message(chat_id=message.from_user.id, text='Сколько часов вы делали эту работу?\n'
                                                                      'Округлите время до получаса')
        else:
            await bot.send_message(chat_id=message.from_user.id, text='How many hours did you do this work?\n'
                                                                      'Round the time up to half an hour')
        await state.set_state(new_calculation.stage_6)





