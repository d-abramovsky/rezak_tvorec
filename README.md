![image](https://github.com/user-attachments/assets/850ef890-d31e-4f76-9de9-3c64f370950a)# Представляем бот компании ТВОРЕЦ by Unibot

[Ознакомится с планом проекта можно по здесь.](https://www.telegram-bot-expert.ru/wp-content/uploads/2024/07/План-работы-ТВОРЕЦ-1.pdf)

Краткие технические характеристики:
*  Язык программирования: Python
*  Взаимодействие с Telegram: Aiogram
*  Базы данных: SQLite3, Redis
*  Шифрование API-ключей: Pyndatic
*  Взаимодействие с Excel: openpyxl
*  Взаимодействие с Google Sheets: pygsheets
*  Взаимодействие с Telegraph: Telegraph API
*  Взаимодействие с Google drive: PyDrive2 

## Структура Базы данных:
### Таблицы
  * admins - Тут хранятся администраторы и их права доступа
  * calculator - Тут отслеживается процесс каклькуляуции каждого пользователя
  * gallery - Тут хранятся данные о фотографиях галлереи, их лайках и кнопках
  * headers - Тут хранятся подразделы, которые загружаются пользователю в меню
  * mailing - Тут записываются данные о рассылках
  * messages - Тут записаны все сообщения, для их дальнейшего анализа
  * products - Тут хранятся данные о товарах
  * referrals - Тут хранятся данные о рефералах
  * translate - Тут записаны переводы для английской версии бота
  * users - Основная таблица с пользователяи и данными о них

## Cтруктура проекта
### Уровни доступа в бот
  * Суперпользователь - имеет все права и управляет всеми функциями в боте
  * Администраторы - управляют ботом в той мере, насколько им хватает прав
  * Пользователи - наслаждаются контентом и не заботятся ни о чем

### Администраторские функции и немного о суперпользователе
Суперпользователь имеет полный контроль над ботом и может выдавать права другим.

Администраторы имеют 4 зоны досупа:
  * Изменение карточек товара и категорий
  * Изменение галлереи
  * Доступ к статистике
  * Доступ к рассылке

### Админ панель

По запросу, администраторы могут посмотреть команды для управления ботом.

![image](https://github.com/user-attachments/assets/ae7bfbec-396c-4e21-a997-3508defc6b39)


### Пагинация
В ботах Unibot реализована уникальная система перелистывания карточек товара. Она строится на хранении "соседей" каждой карточки. Благодаря такой системе, можно быстро редактировать каждый раздел и его наполнение.

![image](https://github.com/user-attachments/assets/1623c9bd-678e-47e8-b2bb-2b655d7f7ae6) 

Пример пагинации в галерее работ. Имеется система лайков и бесконечная прокрутка

![image](https://github.com/user-attachments/assets/cce3de5a-78cb-4224-92d9-168cb7524728)

Пример пагинации карточки товара. Добавлены внешние кнопки, прокрутка имеет конец. 

Карточки имеют возможность изменения. Такая возможность есть у сеперпользователя и администратора с соответсвующими правами.

У администратора есть 3 дополнитлельные кнопки:
  * Добавить следующую
  * Редактировать
  * Удалить

#### Рассмотрим каждую функцию:

##### Добавить следующую
![image](https://github.com/user-attachments/assets/bf37e6b7-7551-4346-b75c-6b6bc96ceb6e)

Начинает опрос пользователя. После спрашивает о типе загрущки фотографии.

![image](https://github.com/user-attachments/assets/28a62bf2-bd6c-405c-a042-acc0006da2e4)

После выбора и загрузки фотографии удобным способом, бот предлагает добавить кнопки.

![image](https://github.com/user-attachments/assets/3d0a5ecb-9deb-477f-906d-8d9ee7402cf3)

Когда карточка сформирована, бот отправляет ее на подтверждение. 

![image](https://github.com/user-attachments/assets/09ade185-66c2-431a-8fe9-32d0f5c788c9)

На этом этапе карточку можно либо изменить, либо завершить добавление. После окончания процесса, карточка получит данные после кого ее нудно открывать и будет добавлена в галерею. 

##### Редактировать
После создания карточку можно изменить.

После нажатия на кнопку, бот отправляет пользователю сообщения, с предложением редактировать карточку.

![image](https://github.com/user-attachments/assets/5a3bcaad-0a8c-4e27-87a7-43de0a08d28f)

После нажатия на кнопку, бот получит информацию об измененном объекте. 

![image](https://github.com/user-attachments/assets/7a1ee469-4418-473d-b5f6-8bb2fee79418)

После этого данные меняются и карточка создается.

##### Удалить
Если карточку нужно удалить, то для этого есть соответсвующая кнопка. При ее нажатии блок с карточками скрывается и появляются кнопки выбора

![image](https://github.com/user-attachments/assets/bdaf6b27-d9c6-4eac-a5f4-a11b02191429)

После выбора кнопки скрываются и можно дальше взаимодействвать с ботом.

![image](https://github.com/user-attachments/assets/831f5171-df47-47af-a3d1-e0d00ebbf23a)


### Статистика
Статистика имеет большую роль в каждом телеграм боте. Unibot собирает данные и преобразовавает их в excel документ.
![image](https://github.com/user-attachments/assets/ed3f5231-b39b-47c3-9192-02fdd1aa920d) 

В данный документ выгружаются основные метрики бота.

### Рассылка

После активации рассылки команжой бот спрашивает ее название.

![image](https://github.com/user-attachments/assets/40fab29c-7a4f-4d2d-af6e-da2395b7e3f9)

После этого бот запрашивает рекламное сообщение

![image](https://github.com/user-attachments/assets/dc93e552-0dcb-434c-90c1-2f0670ff985c)

После получения сообщения бот спрашивает про добавления рекламной кнопки

![image](https://github.com/user-attachments/assets/1017d860-6de3-4034-b01a-c39d0a9a9d87)

Добавим ее!

![image](https://github.com/user-attachments/assets/4a12b5e1-bc62-4797-809a-98d7efdbed74)

После получения данных, бот отправлятет сообщение на согласование

![image](https://github.com/user-attachments/assets/6563856c-cd4d-4bf4-9308-d7f3153de9cf)

После подтверждения бот отправляет соощение всем пользователям

![image](https://github.com/user-attachments/assets/16060f3d-a8e0-47b1-8921-bece0e6a2e6c)

Когда рассылка окончена, юот отправляет результаты. А также грузит данные о рассылке в Google.Sheets

Посмотрим на них!

![image](https://github.com/user-attachments/assets/e0feeb63-7ac6-406e-ae46-8f44e5b32781)

Для добавления администраторов, суперпользователь имеет специальную команду.

![image](https://github.com/user-attachments/assets/32e32070-4c43-4880-a41d-4eabf6bab846)

В ответ бот присылает весь список администраторов.

После нажатия кнопки "Изменить" бот спрашивает о каком администраторе идет речь

![image](https://github.com/user-attachments/assets/39439a71-a643-4ff3-afb0-265a16b67cdf)

Затем появляется меню выдачи прав

![image](https://github.com/user-attachments/assets/808d64e3-ac11-4ae7-b222-8c7e3e04de08)

После выдачи всех прав, бот возвращается обратно в меню

![image](https://github.com/user-attachments/assets/53eee10d-4134-43e7-af11-29efc625adce)

![image](https://github.com/user-attachments/assets/3a4518e2-05d2-4f1c-baf5-8900915d12a7)











