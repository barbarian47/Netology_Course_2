import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from auth_data import api_group_key, VK_TOKEN
from vk_search import get_list, client_info
from vk_get_photo import create_top_photo_list
from db_write_request_in import write_in_bd, write_in_blacklist, write_count
from db_select import select_favorit_users_from_bd, all_clients, select_count


vk_session = vk_api.VkApi(token=api_group_key)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

users_requests = dict()
client_match = dict()


def send_msg(id, text, keyboard=None):
    """
    Функция отправляет сообщение собеседнику

    :param id: id собеседника
    :type id: int
    :param text: текст сообщения
    :type : str
    :param keyboard: клавиатура с необходимыми кнопками
    :type : class instance 'vk_api.keyboard.VkKeyboard'
    """
    message = {
        'user_id': id,
        'message': text,
        'random_id': 0
    }

    if keyboard != None:
        message['keyboard'] = keyboard.get_keyboard()

    vk_session.method('messages.send', message)


def get_start(id):
    """
    Функция отправляет кнопку предлагающую начать подбор

    :param id: id собеседника
    :type id: int
    """
    fav_list = select_favorit_users_from_bd(id)
    name = client_info(id)['response'][0]['first_name']
    if len(fav_list) > 0:
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Начнём подбор!', VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('ИЗБРАННОЕ', VkKeyboardColor.PRIMARY)
        keyboard.add_button('Дальше', VkKeyboardColor.SECONDARY)
        send_msg(id, f'Привет, {name}', keyboard)
    else:
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Начнём подбор!', VkKeyboardColor.PRIMARY)
        send_msg(id, f'Привет, {name}', keyboard)


def get_finish(id):
    """
    Функция отправляет сообщение при завершении сеанса общения

    :param id: id собеседника
    :type id: int
    """
    name = client_info(id)['response'][0]['first_name']
    send_msg(id, f'Пока, {name}! Возвращайтесь!')


def get_city(id):
    """
    Функция отправляет сообщение с просьбой ввести город в котором будем искать

    :param id: id собеседника
    :type id: int
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, 'В каком городе будем искать?', keyboard)


def confirm_city(id, city):
    """
    Функция отправляет кнопки для изменения и подтверждения города

    :param id: id собеседника
    :type id: int
    :param city: название города которое ввёл собеседник
    :type city: str
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Да, город верный', VkKeyboardColor.POSITIVE)
    keyboard.add_button('Изменить город', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, f'Ищем по городу {city.title()}?', keyboard)


def get_sex(id):
    """
    Функция отправляет кнопки для выбора пола партнёра

    :param id: id собеседника
    :type id: int
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Парня', VkKeyboardColor.SECONDARY)
    keyboard.add_button('Девушку', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, 'Кого будем искать?', keyboard)


def get_age_from(id):
    """
    Функция отправляет сообщение с запросом возраста с которого будет вестись поиск

    :param id: id собеседника
    :type id: int
    """
    send_msg(id, 'Со скольки лет?')


def get_age_to(id):
    """
    Функция отправляет сообщение с запросом возраста до которого будет вестись поиск

    :param id: id собеседника
    :type id: int
    """
    send_msg(id, 'До скольки лет?')


def confirm_data(id, city, sex, age_from, age_to):
    """
    Функция отправляет кнопки для изменения и подтверждения параметров поиска

    :param id: id собеседника
    :type id: int
    :param city: название города
    :type city: str
    :param sex: пол партнёра
    :type sex: str
    :param age_from: нижняя планка возраста
    :type age_from: int
    :param age_to: верхняя планка возраста
    :type age_to: int
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Всё верно', VkKeyboardColor.SECONDARY)
    keyboard.add_button('Изменить параметры', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, f'Ищем {sex} в возрасте от {age_from} до {age_to} из города {city.title()}?', keyboard)


def change_data(id):
    """
    Функция отправляет кнопки для выбора параметра который необходимо изменить

    :param id: id собеседника
    :type id: int
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Город', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Пол', VkKeyboardColor.POSITIVE)
    keyboard.add_button('Возраст', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, 'Что хотите изменить?', keyboard)


def send_match(id, text):
    """
    Функция отправляет сообщение с количеством совпадений и кнопку для начала просмотра

    :param id: id собеседника
    :type id: int
    :param text: количество совпадений по заданным параметрам
    :type text: int
    """
    if text > 0:
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Давай смотреть!', VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
        send_msg(id, f'По Вашему запросу найдено {text} совпадений.', keyboard)
    else:
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Начнём подбор!', VkKeyboardColor.PRIMARY)
        send_msg(id, 'Нет совпадений. Давайте изменим параметры подбора!', keyboard)


def get_token(id):
    """
    Функция отправляет кнопки для выяснения наличия токена доступа

    :param id: id собеседника
    :type id: int
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Есть токен', VkKeyboardColor.POSITIVE)
    keyboard.add_button('Нет токена', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, 'У Вас есть токен ВК?', keyboard)


def send_photo(id, url):
    """
    Функция отправляет фотографию

    :param id: id собеседника
    :type id: int
    :param url: вложение
    :type url: str
    """
    vk.messages.send(user_id=id, attachment=url, random_id=0)


def send_person(id, current_match, token=VK_TOKEN):
    """
    Функция отправляет сообщения с данными о партнёре и навигационные кнопки

    вызывает функцию с получением данных о фото, формирует ссылки на фото

    :param id: id собеседника
    :type id: int
    :param current_match: словарь с данными о текущем партнёре
    :type current_match: dict
    :param token: токен доступа
    :type token: str

    :return current_data: словарь с данными о пользователя и 3 самые популярные фото
    :type current_data: dict
    """
    current_data = create_top_photo_list(current_match, token)
    full_name = current_data['first_name'] + ' ' + current_match['last_name']
    link = current_data['link']
    send_msg(id, full_name)
    send_msg(id, link)
    for photo in current_data['photo']:
        url = f"photo{current_data['partner_id']}_{photo[0]}"
        send_photo(id=id, url=url)

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('В чёрный список', VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Дальше', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('ИЗБРАННОЕ', VkKeyboardColor.PRIMARY)
    keyboard.add_button('В избранное', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, f'Как Вам {full_name}?', keyboard)

    return current_data


def add_to_favorite(id, user_info):
    """
    Функция добавляет партнера в избранное и записывает в БД

    :param id: id собеседника
    :type id: int
    :param user_info: словарь с данными о пользователя и 3 самые популярные фото
    :type user_info: dict
    """
    write_in_bd(id, user_info)
    full_name = user_info['first_name'] + ' ' + user_info['last_name']

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('ИЗБРАННОЕ', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Дальше', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, f'{full_name} в избранном!', keyboard)


def list_is_over(id):
    """
    Функция отправляет сообщение о том что список совпадений закончился и навигационные кнопки

    :param id: id собеседника
    :type id: int
    """
    send_msg(id, 'По данному запросу ничего больше нет(')
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('ИЗБРАННОЕ', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Начнём подбор!', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, 'Начнём новый подбор?', keyboard)


def show_favorite(id):
    """
    Функция отправляет сообщения с данными о списке избранных получив данные из БД

    :param id: id собеседника
    :type id: int
    """
    fav_list = select_favorit_users_from_bd(id)
    send_msg(id, f'У Вас в избранном {len(fav_list)} человек:')
    for key in fav_list:
        full_name = fav_list[key][0] + ' ' + fav_list[key][1]
        link = fav_list[key][2]
        send_msg(id, f'{full_name} --> {link}')

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Дальше', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, 'Смотрим дальше?', keyboard)


def add_to_blacklist(id, current_match):
    """
    Функция добавляет пользователя в черный список и делает запись в БД

    :param id: id собеседника
    :type id: int
    :param current_match: словарь с данными о пользователе
    :type current_match: dict
    """
    full_name = current_match['first_name'] + ' ' + current_match['last_name']

    write_in_blacklist(id_client=id, id_partner=current_match['id'])

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('ИЗБРАННОЕ', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Дальше', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, f'{full_name} добавлена в чёрный список и больше не будет появляться в выдаче!', keyboard)


flag = ''
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        client_id = event.user_id
        if msg and flag == '':
            clients = all_clients()
            if client_id in clients:
                last_session = select_count(client_id)
                count = last_session[1]
                users_requests[client_id] = last_session[2]
                client_match[client_id] = get_list(id=client_id, users_requests=users_requests[client_id])
                match_count = len(client_match[client_id])
                if last_session[2]['token'] == '':
                    token = VK_TOKEN
                else:
                    token = last_session[2]['token']
            get_start(client_id)
            flag = 'start'
        if msg == 'завершить общение :(':
            param = f'{{"city": "{users_requests[client_id]["city"]}", "sex": "{users_requests[client_id]["sex"]}", '
            param += f'"age_from": "{users_requests[client_id]["age_from"]}", "age_to": '
            param += f'"{users_requests[client_id]["age_to"]}", "token": "{users_requests[client_id]["token"]}"}}'
            write_count(client_id, count, param)
            get_finish(client_id)
            flag = ''
        elif msg == 'начнём подбор!':
            users_requests[client_id] = {"city": "", "sex": "", "age_from": "", "age_to": "", "token": ""}
            get_city(client_id)
            flag = 'to_city'
        elif flag == 'to_city':
            confirm_city(client_id, msg)
            flag = msg
        elif msg == 'да, город верный' and flag != 'confirm data':
            city = flag
            users_requests[client_id]["city"] = city
            flag = 'to_sex'
            get_sex(client_id)
        elif msg == 'изменить город':
            get_city(client_id)
            if users_requests[client_id]["sex"] == "":
                flag = 'to_city'
            else:
                flag = 'change city'
        elif msg == 'парня' and flag != 'change sex':
            sex = msg
            users_requests[client_id]["sex"] = 2
            get_age_from(client_id)
            flag = 'to_age_f'
        elif msg == 'девушку' and flag != 'change sex':
            sex = msg
            users_requests[client_id]["sex"] = 1
            get_age_from(client_id)
            flag = 'to_age_f'
        elif flag == 'to_age_f':
            try:
                age_f = int(msg.strip())
                users_requests[client_id]["age_from"] = age_f
                get_age_to(client_id)
                flag = 'to_age_t'
            except ValueError:
                send_msg(client_id, 'Что-то пошло не так')
                get_age_from(client_id)
        elif flag == 'to_age_t':
            try:
                age_t = int(msg.strip())
                users_requests[client_id]["age_to"] = age_t
                flag = 'confirm'
                confirm_data(id=client_id, city=city, sex=sex, age_from=age_f, age_to=age_t)
            except ValueError:
                send_msg(client_id, 'Что-то пошло не так')
                get_age_from(client_id)
        elif msg == 'всё верно':
            get_token(client_id)
        elif msg == 'есть токен':
            flag = msg
            send_msg(client_id, 'Введите свой токен ВК:')
        elif flag == 'есть токен':
            users_requests[client_id]["token"] = msg
            send_msg(client_id, 'Алгоритм работает! Это может занять какое-то время!')
            client_match[client_id] = get_list(id=client_id, users_requests=users_requests[client_id])
            if client_match[client_id] != 'Ошибка токена':
                match_count = len(client_match[client_id])
                send_match(client_id, match_count)
                flag = 'confirm'
            else:
                send_msg(client_id, 'Ошибка токена')
                users_requests[client_id]["token"] = ""
                flag = 'confirm'
                get_token(client_id)
        elif msg == 'нет токена':
            send_msg(client_id, 'Алгоритм работает! Это может занять какое-то время!')
            client_match[client_id] = get_list(id=client_id, users_requests=users_requests[client_id])
            match_count = len(client_match[client_id])
            send_match(client_id, match_count)
        elif msg == 'изменить параметры':
            change_data(client_id)
        elif msg == 'город':
            get_city(client_id)
            flag = 'change city'
        elif flag == 'change city':
            flag = 'confirm data'
            new_city = msg
            confirm_city(client_id, msg)
        elif msg == 'да, город верный' and flag == 'confirm data':
            city = new_city
            users_requests[client_id]["city"] = city
            confirm_data(id=client_id, city=city, sex=sex, age_from=age_f, age_to=age_t)
        elif msg == 'возраст':
            get_age_from(client_id)
            flag = 'to_age_f'
        elif msg == 'пол':
            flag = 'change sex'
            get_sex(client_id)
        elif msg == 'парня' and flag == 'change sex':
            sex = msg
            users_requests[client_id]["sex"] = 2
            confirm_data(id=client_id, city=city, sex=sex, age_from=age_f, age_to=age_t)
        elif msg == 'девушку' and flag == 'change sex':
            sex = msg
            users_requests[client_id]["sex"] = 1
            confirm_data(id=client_id, city=city, sex=sex, age_from=age_f, age_to=age_t)
        elif msg == 'давай смотреть!':
            count = 0
            param = f'{{"city": "{users_requests[client_id]["city"]}", "sex": "{users_requests[client_id]["sex"]}", '
            param += f'"age_from": "{users_requests[client_id]["age_from"]}", "age_to": '
            param += f'"{users_requests[client_id]["age_to"]}", "token": "{users_requests[client_id]["token"]}"}}'
            write_count(client_id, count, param)
            current_match = client_match[client_id][count]
            if users_requests[client_id]["token"]:
                token = users_requests[client_id]["token"]
            else:
                token = VK_TOKEN
            user_info = send_person(client_id, current_match, token)
        elif msg == 'дальше':
            count += 1
            if count < match_count:
                current_match = client_match[client_id][count]
                user_info = send_person(client_id, current_match, token)
            else:
                list_is_over(client_id)
        elif msg == 'в избранное':
            add_to_favorite(id=client_id, user_info=user_info)
        elif msg == 'избранное':
            show_favorite(client_id)
        elif msg == 'в чёрный список':
            add_to_blacklist(client_id, current_match)
