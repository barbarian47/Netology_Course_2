# VKinder51

## Командный проект по курсу «Профессиональная работа с Python»
_____
### Описание проекта
*VKinder51* - это чат бот для ВКонтакте который подбирает пользователей по заданным параметрам.

Возможности бота:
* Управление кнопками
* Подбор по параметрам
* Отправка самых популрных фото
* Добавление в избранное
* Добавление в черный список

Параметры поиска(возможность расширения):
* Город
* Пол
* Возраст

Команды для общения с ботом:
* ***Начать подбор*** - запускает опрос пользователя для получения параметров поиска
* ***Давай смотреть!*** - начать просмотр результатов подбора
* ***В избранное*** - добавляет последнего пользователя в список избранных, делает забись в БД
* ***В черный список*** - добавляет последнего пользователя в черный список, делает забись в БД, пользователь больше не будет появляться в результатах подбора
* ***Избранное*** - отправляет список имён и ссылок на аккаунты всех пользователей из списка избранных
* ***Дальше*** - перейти к следующему пользователю
* ***Завершить общение*** - заканчивает сессию общения и сохраняет текущую точку просмотра результатов подбора

___
## Запуск проекта
Запуск БД:
* создать БД на своей машине
* заполинть данные в файле ***config.py***
* запустить файл ***db_create.py***

Запуск бота ВК:
* создать группу ВКотакте
* в настройках группы(Работа с API) получить ключ доступа
* создать Standalone-приложение и получить токен доступа
* в файл ***auth_data.py*** ввести полученные данные
* установить библиотеки из файла ***requirements.txt***
* запустить файл ***vk_bot_messenger.py***