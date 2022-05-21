import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from auth_data import api_group_key, VK_TOKEN
from vk_search import get_list
from vk_get_photo import create_top_photo_list
#from db_write_ request_in import write_in_bd
from pprint import pprint


vk_session = vk_api.VkApi(token=api_group_key)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

users_requests = dict()
client_match = dict()


def send_msg(id, text, keyboard=None):
    message = {
        'user_id': id,
        'message': text,
        'random_id': 0
    }

    if keyboard != None:
        message['keyboard'] = keyboard.get_keyboard()

    vk_session.method('messages.send', message)


def get_start(id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Начнём подбор!', VkKeyboardColor.PRIMARY)
    send_msg(id, 'Доброго времени суток!', keyboard)


def get_finish(id):
    send_msg(id, 'Пока! Возвращайтесь!')


def get_city(id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, 'В каком городе будем искать?', keyboard)


def confirm_city(id, city):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Да, город верный', VkKeyboardColor.POSITIVE)
    keyboard.add_button('Изменить город', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, f'Ищем по городу {city.title()}?', keyboard)


def get_sex(id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Парня', VkKeyboardColor.SECONDARY)
    keyboard.add_button('Девушку', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, 'Кого будем искать?', keyboard)


def get_age_from(id):
    send_msg(id, 'Со скольки лет?')


def get_age_to(id):
    send_msg(id, 'До скольки лет?')


def confirm_data(id, city, sex, age_from, age_to):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Всё верно', VkKeyboardColor.SECONDARY)
    keyboard.add_button('Изменить параметры', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, f'Ищем {sex} в возрасте от {age_from} до {age_to} из города {city.title()}?', keyboard)


def change_data(id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Город', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Пол', VkKeyboardColor.POSITIVE)
    keyboard.add_button('Возраст', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, 'Что хотите изменить?', keyboard)


def send_match(id, text):
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


def send_photo(id, url):
    vk.messages.send(user_id=id, attachment=url, random_id=0)


def send_person(id, current_match, token):
    current_data = create_top_photo_list(current_match, token)
#    pprint(current_data)
    full_name = current_data['first_name'] + ' ' + current_match['last_name']
    link = current_data['link']
    send_msg(id, full_name)
    send_msg(id, link)
    for photo in current_data['photo']:
        url = f"photo{current_data['partner_id']}_{photo[0]}"
        send_photo(id=id, url=url)

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('ИЗБРАННОЕ', VkKeyboardColor.PRIMARY)
    keyboard.add_button('В избранное', VkKeyboardColor.POSITIVE)
    keyboard.add_button('Дальше', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, f'Как Вам {full_name}?', keyboard)

    return current_data


def add_to_favorite(id, user_info):
#    write_in_bd(id, user_info)
    full_name = user_info['first_name'] + ' ' + user_info['last_name']

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('ИЗБРАННОЕ', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Дальше', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, f'{full_name} в избранном!', keyboard)


def list_isover(id):
    send_msg(id, 'По данному запросу ничего больше нет(')
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('ИЗБРАННОЕ', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Начнём подбор!', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, 'Начнём новый подбор?', keyboard)


flag = ''
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        client_id = event.user_id

        if msg and client_id not in users_requests and flag == '':
            get_start(client_id)
            flag = 'start'
        if msg == 'завершить общение :(':
            get_finish(client_id)
            del users_requests[client_id]
            flag = ''
        elif msg == 'начнём подбор!':
            users_requests[client_id] = {'city': '', 'sex': '', 'age_from': '', 'age_to': '', 'token': ''}
            get_city(client_id)
            flag = 'to_city'
        elif flag == 'to_city':
            confirm_city(client_id, msg)
            flag = msg
        elif msg == 'да, город верный' and flag != 'confirm data':
            city = flag
            users_requests[client_id]['city'] = city
            flag = 'to_sex'
            get_sex(client_id)
        elif msg == 'изменить город':
            get_city(client_id)
            if users_requests[client_id]['sex'] == '':
                flag = 'to_city'
            else:
                flag = 'change city'
        elif msg == 'парня' and flag != 'change sex':
            sex = msg
            users_requests[client_id]['sex'] = 2
            get_age_from(client_id)
            flag = 'to_age_f'
        elif msg == 'девушку' and flag != 'change sex':
            sex = msg
            users_requests[client_id]['sex'] = 1
            get_age_from(client_id)
            flag = 'to_age_f'
        elif flag == 'to_age_f':
            try:
                age_f = int(msg.strip())
                users_requests[client_id]['age_from'] = age_f
                get_age_to(client_id)
                flag = 'to_age_t'
            except ValueError:
                send_msg(client_id, 'Что-то пошло не так')
                get_age_from(client_id)
        elif flag == 'to_age_t':
            try:
                age_t = int(msg.strip())
                users_requests[client_id]['age_to'] = age_t
                flag = 'confirm'
                confirm_data(id=client_id, city=city, sex=sex, age_from=age_f, age_to=age_t)
            except ValueError:
                send_msg(client_id, 'Что-то пошло не так')
                get_age_from(client_id)
        elif msg == 'всё верно':
            send_msg(client_id, 'Алгоритм работает! Это может занять какое-то время!')
#            print(users_requests)
            client_match[client_id] = get_list(client_id=client_id, users_requests=users_requests[client_id])
#            print(client_match[client_id])
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
            users_requests[client_id]['city'] = city
            confirm_data(id=client_id, city=city, sex=sex, age_from=age_f, age_to=age_t)
        elif msg == 'возраст':
            get_age_from(client_id)
            flag = 'to_age_f'
        elif msg == 'пол':
            flag = 'change sex'
            get_sex(client_id)
        elif msg == 'парня' and flag == 'change sex':
            sex = msg
            users_requests[client_id]['sex'] = 2
            confirm_data(id=client_id, city=city, sex=sex, age_from=age_f, age_to=age_t)
        elif msg == 'девушку' and flag == 'change sex':
            sex = msg
            users_requests[client_id]['sex'] = 1
            confirm_data(id=client_id, city=city, sex=sex, age_from=age_f, age_to=age_t)
        elif msg == 'давай смотреть!':
#            pprint(client_match[client_id])
            count = 0
            current_match = client_match[client_id][count]
            if users_requests[client_id]['token']:
                token = users_requests[client_id]['token']
            else:
                token = VK_TOKEN
            user_info = send_person(client_id, current_match, token)
        elif msg == 'дальше':
            count += 1
            if count < match_count:
                current_match = client_match[client_id][count]
                user_info = send_person(client_id, current_match, token)
            else:
                list_isover(client_id)
        elif msg == 'в избранное':
            add_to_favorite(id=client_id, user_info=user_info)

        #
        # print(users_requests)
        # print(flag)
        # print(msg)
