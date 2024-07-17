from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Выбрать резаки'),
            KeyboardButton(text='Выбрать аксессуары')
        ],
        [
            KeyboardButton(text='Выбрать цифровые продукты'),
            KeyboardButton(text='Выбрать расходные материалы')
        ],
        [
            KeyboardButton(text='Госучреждениям'),
            KeyboardButton(text='Галерея работ')
        ],
        [
            KeyboardButton(text='Калькулятор расчета стоимости фигуры'),
        ],
    ],
    resize_keyboard=True, input_field_placeholder='Главное меню'
)

keyboard_eng = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Choose cutters'),
            KeyboardButton(text='Choose accessories')
        ],
        [
            KeyboardButton(text='Choose consumables'),
            KeyboardButton(text='Gallery')
        ],
        [
            KeyboardButton(text='Figure cost calculator'),
        ],
    ],
    resize_keyboard=True, input_field_placeholder='Main menu'
)

change_section = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Добавить новый раздел'),
            KeyboardButton(text='Удалить раздел'),
        ],
        [
            KeyboardButton(text='Вернуться в главное меню'),
        ],
    ],
    resize_keyboard=True, input_field_placeholder='Изменить разделы'
)

web = WebAppInfo(url='https://d-abramovsky.github.io/')
rezak = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Художественная резка'),
            KeyboardButton(text='Техническая резка')
        ],
        [
            KeyboardButton(text='Полный каталог резаков', web_app=web)
        ],
        [
            KeyboardButton(text='Вернуться в главное меню'),
        ],
    ],
    resize_keyboard=True
)

rezak_eng = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Artistic cutting'),
            KeyboardButton(text='Technical cutting')
        ],
        [
            KeyboardButton(text='Catalog of cutters', web_app=web)
        ],
        [
            KeyboardButton(text='Return to the main menu'),
        ],
    ],
    resize_keyboard=True
)

skip = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Нет'
        )
    ]
], resize_keyboard=True, input_field_placeholder='Кнопки не будет?')


phone = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Отправить номер 📞',
            request_contact = True
        )
    ]
], resize_keyboard=True,)

percent = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='25'),
            KeyboardButton(text='50'),
            KeyboardButton(text='75'),
            KeyboardButton(text='100'),

        ],
    ],
    resize_keyboard=True
)


