from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

confirm = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Название', callback_data= 'name_change'),
            InlineKeyboardButton(text='Описание', callback_data='description_change'),
            InlineKeyboardButton(text='Фото', callback_data='photo_change'),
            InlineKeyboardButton(text='Кнопки', callback_data='button_change'),
        ],
        [
            InlineKeyboardButton(text='Опубликовать ✅', callback_data='good_job'),
        ]
    ],
)

update_product= InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Название', callback_data= 'name_change'),
            InlineKeyboardButton(text='Описание', callback_data='description_change'),
            InlineKeyboardButton(text='Фото', callback_data='photo_change'),
            InlineKeyboardButton(text='Кнопки', callback_data='button_change'),
        ],
    ],
)

confirm_gallery = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Название', callback_data= 'name_change'),
            InlineKeyboardButton(text='Фото', callback_data='photo_change'),
            InlineKeyboardButton(text='Кнопки', callback_data='button_change'),
        ],
        [
            InlineKeyboardButton(text='Опубликовать ✅', callback_data='good_job'),
        ]
    ],
)

update_gallery= InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Название', callback_data= 'name_change'),
            InlineKeyboardButton(text='Фото', callback_data='photo_change'),
            InlineKeyboardButton(text='Кнопки', callback_data='button_change'),
        ],
    ],
)

photo = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Ссылка на фото 🔗', callback_data= 'photo_link'),
            InlineKeyboardButton(text='Загрузить фото 🖼', callback_data='upload_photo')

        ],
    ],
)

admin_keyboard_change_level = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Изменить права', callback_data= 'change_admin_level')
        ],
    ],
)

gos = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Перейти и ознакомится', url="https://www.rezak-penoplasta-tvorec.ru/kindergartens/")
        ],
    ],
)

calculator = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Налог', callback_data= 'calc_tax'),
            InlineKeyboardButton(text='Амортизация', callback_data= 'calc_amortization'),

        ],
        [
            InlineKeyboardButton(text='Стоимость работы', callback_data='calc_work'),
            InlineKeyboardButton(text='Прибыль', callback_data='calc_profit')
        ],
        [
            InlineKeyboardButton(text='Продолжить ✅', callback_data='calc_hour')
        ],
    ],
)

calculator_eng = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Taxes', callback_data= 'calc_tax'),
            InlineKeyboardButton(text='Amortization', callback_data= 'calc_amortization'),

        ],
        [
            InlineKeyboardButton(text='Work cost', callback_data='calc_work'),
            InlineKeyboardButton(text='Profit', callback_data='calc_profit')
        ],
        [
            InlineKeyboardButton(text='Complete ✅', callback_data='calc_hour')
        ],
    ],
)

acrylic = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да ✅', callback_data= 'acryl_1'),
            InlineKeyboardButton(text='Нет ❌', callback_data= 'acryl_0')

        ],
    ],
)

acrylic_eng = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Yes ✅', callback_data= 'acryl_1'),
            InlineKeyboardButton(text='No ❌', callback_data= 'acryl_0')

        ],
    ],
)

delete = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да ✅', callback_data= 'del_1'),
            InlineKeyboardButton(text='Нет ❌', callback_data= 'del_0')

        ],
    ],
)

mailing_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да ✅', callback_data= 'mail_1'),
            InlineKeyboardButton(text='Нет ❌', callback_data= 'mail_0')

        ],
    ],
)

confirm_mailing_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Подтверждаю отправку ✅', callback_data= 'confirm_mail')
        ],
        [
            InlineKeyboardButton(text='Отменить рассылку ❌', callback_data='finish_state')
        ],
    ],
)

gallery_delete = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да ✅', callback_data= 'gallery_del_1'),
            InlineKeyboardButton(text='Нет ❌', callback_data= 'gallery_del_0')

        ],
    ],
)

confirm_poll = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да ✅', callback_data= 'poll_1'),
            InlineKeyboardButton(text='Нет ❌', callback_data= 'poll_0')

        ],
    ],
)

web = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Посетите наш сайт',
            url='https://www.rezak-penoplasta-tvorec.ru/'
        ),
    ],
])

deactivate = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Отменить ❌', callback_data='finish_state')
    ],
])

deactivate_eng = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Cancel ❌', callback_data='finish_state')
    ],
])

def like_keyboard(likes, user_id, uin, builder, counter):
    if (len(likes) > 0) and (str(likes).count(' ')) > 0:
        if str(user_id) in likes:
            return builder.button(text=f'️{counter} ❤️', callback_data=f'like{uin}',)
        else:
            return builder.button(text=f'️{counter} 🤍', callback_data=f'like{uin}')
    elif str(likes) == str(user_id):
        return builder.button(text=f'{counter} ❤️', callback_data=f'like{uin}')
    else:
        return builder.button(text=f'️{counter} 🤍', callback_data=f'like{uin}')

def admin_keyboard(prv, nxt, uin, builder):
    if prv == 'Начало':
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
        return builder.attach(InlineKeyboardBuilder.from_markup(page))
    else:
        page = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Добавить следующую карту", callback_data=f'gnc{uin}'),
                ],
                [
                    InlineKeyboardButton(text="Изменить текущую карту", callback_data=f'glch{uin}'),
                ],
                [
                    InlineKeyboardButton(text="Удалить текущую карту", callback_data=f'gdl{uin}{nxt}{prv}')
                ],
            ],
        )
        return builder.attach(InlineKeyboardBuilder.from_markup(page))

def settings(politics, lang):
    builder = InlineKeyboardBuilder()
    if politics == 1:
        builder.button(text='Имя/Фамилия', callback_data='name/last') if lang == 'RU' else builder.button(text='Name/Surname', callback_data='name/last')
        builder.button(text='Возраст', callback_data='age') if lang == 'RU' else builder.button(text='Age', callback_data='age')
        builder.button(text='Номер телефона ☎️', callback_data='phone') if lang == 'RU' else builder.button(text='Phone number ☎️', callback_data='phone')
        builder.button(text='Почта 📨', callback_data='email') if lang == 'RU' else builder.button(text='E-mail 📨', callback_data='email')
        builder.button(text='Как вы узнали о компании ТВОРЕЦ?', callback_data='poll') if lang == 'RU' else builder.button(text='How did you find out about the TVOREC?', callback_data='poll')
        builder.adjust(2, 2, 1)
        land_builder = InlineKeyboardBuilder()
        land_builder.button(text='Рус/RU 🇷🇺', callback_data='lang_RU')
        land_builder.button(text='Англ/EN 🇬🇧', callback_data='lang_EN')
        land_builder.button(text='Убрать меню ❌', callback_data='setdestroy') if lang == 'RU' else land_builder.button(text='Close settings ❌', callback_data='setdestroy')
        land_builder.adjust(2, 1)
        builder.attach(land_builder)
    else:
        builder.button(text='Согласен ✅', callback_data='polit') if lang == 'RU' else builder.button(text='I agree ✅', callback_data='polit')
    return builder.as_markup()


materials = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Пенопласт', callback_data='&styrofoam'),
                InlineKeyboardButton(text='Потолочная плитка', callback_data='&roof'),

            ],
            [
                InlineKeyboardButton(text='Экструдированный пенополистерол', callback_data='&expanded'),
            ],
            [
                InlineKeyboardButton(text='Грунт', callback_data='&priming'),
                InlineKeyboardButton(text='Акриловая краска', callback_data='&acrylic'),
            ],
            [
                InlineKeyboardButton(text='Лак', callback_data='&varnish'),
                InlineKeyboardButton(text='Клей', callback_data='&glue'),
            ],
            [
                InlineKeyboardButton(text='Другие материалы', callback_data='&materials'),
            ],
            [
                InlineKeyboardButton(text='Завершить выбор материала ✅', callback_data='save'),
            ],
        ])

materials_eng = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Styrofoam', callback_data='&styrofoam'),
                InlineKeyboardButton(text='Ceiling tiles', callback_data='&roof'),

            ],
            [
                InlineKeyboardButton(text='Extruded polystyrene foam', callback_data='&expanded'),
            ],
            [
                InlineKeyboardButton(text='Primer', callback_data='&priming'),
                InlineKeyboardButton(text='Acrylic paint', callback_data='&acrylic'),
            ],
            [
                InlineKeyboardButton(text='Varnish', callback_data='&varnish'),
                InlineKeyboardButton(text='Glue', callback_data='&glue'),
            ],
            [
                InlineKeyboardButton(text='Other materials', callback_data='&materials'),
            ],
            [
                InlineKeyboardButton(text='Complete ✅', callback_data='save'),
            ],
        ])

def calculator_choose_mat(new_state, lang):
    builder = InlineKeyboardBuilder()
    if lang == 'RU':
        if new_state[1] == 'styrofoam':
            builder.button(text='🔘Пенопласт', callback_data='&styrofoam')
        else:
            builder.button(text='Пенопласт', callback_data='&styrofoam')
        if new_state[3] == 'roof':
            builder.button(text='🔘Потолочная плитка', callback_data='&roof')
        else:
            builder.button(text='Потолочная плитка', callback_data='&roof')
        if new_state[2] == 'expanded':
            builder.button(text='🔘Экструдированный пенополистерол', callback_data='&expanded')
        else:
            builder.button(text='Экструдированный пенополистерол', callback_data='&expanded')
        if new_state[5] == 'priming':
            builder.button(text='🔘Грунт', callback_data='&priming')
        else:
            builder.button(text='Грунт', callback_data='&priming')
        if new_state[6] == 'acrylic':
            builder.button(text='🔘Акриловая краска', callback_data='&acrylic')
        else:
            builder.button(text='Акриловая краска', callback_data='&acrylic')
        if new_state[7] == 'varnish':
            builder.button(text='🔘Лак', callback_data='&varnish')
        else:
            builder.button(text='Лак', callback_data='&varnish')
        if new_state[4] == 'glue':
            builder.button(text='🔘Клей', callback_data='&glue')
        else:
            builder.button(text='Клей', callback_data='&glue')
        if new_state[8] == 'materials':
            builder.button(text='🔘Другие материалы', callback_data='&materials')
        else:
            builder.button(text='Другие материалы', callback_data='&materials')
        builder.button(text='Завершить выбор материала ✅', callback_data='save')
        builder.adjust(2, 1, 2, 2, 1, 1)
        return builder.as_markup()
    else:
        if new_state[1] == 'styrofoam':
            builder.button(text='🔘Styrofoam', callback_data='&styrofoam')
        else:
            builder.button(text='Styrofoam', callback_data='&styrofoam')
        if new_state[3] == 'roof':
            builder.button(text='🔘Ceiling tiles', callback_data='&roof')
        else:
            builder.button(text='Ceiling tiles', callback_data='&roof')
        if new_state[2] == 'expanded':
            builder.button(text='🔘Extruded polystyrene foam', callback_data='&expanded')
        else:
            builder.button(text='Extruded polystyrene foam', callback_data='&expanded')
        if new_state[5] == 'priming':
            builder.button(text='🔘Primer', callback_data='&priming')
        else:
            builder.button(text='Primer', callback_data='&priming')
        if new_state[6] == 'acrylic':
            builder.button(text='🔘Acrylic paint', callback_data='&acrylic')
        else:
            builder.button(text='Acrylic paint', callback_data='&acrylic')
        if new_state[7] == 'varnish':
            builder.button(text='🔘Varnish', callback_data='&varnish')
        else:
            builder.button(text='Varnish', callback_data='&varnish')
        if new_state[4] == 'glue':
            builder.button(text='🔘Glue', callback_data='&glue')
        else:
            builder.button(text='Glue', callback_data='&glue')
        if new_state[8] == 'materials':
            builder.button(text='🔘Other materials', callback_data='&materials')
        else:
            builder.button(text='Other materials', callback_data='&materials')
        builder.button(text='Complete ✅', callback_data='save')
        builder.adjust(2, 1, 2, 2, 1, 1)
        return builder.as_markup()
def admin_change_level_key(admin_id, menu, gallery, mailing, statistics):
    builder = InlineKeyboardBuilder()
    if menu == '1':
            builder.button(text='🔘 Доступ к карточкам товара и категориям', callback_data=f'adm:card:{admin_id}')
    else:
            builder.button(text='Доступ к карточкам товара и категориям', callback_data=f'adm:card:{admin_id}')
    if gallery == '1':
        builder.button(text='🔘 Доступ к галерее', callback_data=f'adm:gall:{admin_id}')
    else:
        builder.button(text='Доступ к галерее', callback_data=f'adm:gall:{admin_id}')
    if mailing == '1':
            builder.button(text='🔘 Доступ к рассылке', callback_data=f'adm:mail:{admin_id}')
    else:
            builder.button(text='Доступ к рассылке', callback_data=f'adm:mail:{admin_id}')
    if statistics == '1':
        builder.button(text='🔘 Доступ к статистике', callback_data=f'adm:stat:{admin_id}')
    else:
        builder.button(text='Доступ к статистике', callback_data=f'adm:stat:{admin_id}')
    builder.button(text='Завершить изменения ✅', callback_data=f'adm:stop')
    builder.adjust(1)
    return builder.as_markup()