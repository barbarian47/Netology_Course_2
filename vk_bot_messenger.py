import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from auth_data import api_group_key

vk_session = vk_api.VkApi(token=api_group_key)
longpoll = VkLongPoll(vk_session)

users_requests = dict()


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
    keyboard.add_line()
    keyboard.add_button('Возраст от', VkKeyboardColor.SECONDARY)
    keyboard.add_button('Возраст до', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, 'Что хотите изменить?', keyboard)


last_msg = ''
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        client_id = event.user_id

        if 'hi' in msg:
            get_start(client_id)
            last_msg = ''
        if msg == 'начнём подбор!':
            users_requests[client_id] = {'city': '', 'sex': '', 'age_from': '', 'age_to': ''}
            get_city(client_id)
            last_msg = 'начнём подбор!'
        elif last_msg == 'начнём подбор!':
            confirm_city(client_id, msg)
            last_msg = msg
        if msg == 'да, город верный':
            city = last_msg
            users_requests[client_id]['city'] = last_msg
            last_msg = 'город'
        if msg == 'изменить город':
            get_city(client_id)
            last_msg = 'начнём подбор!'
        if last_msg == 'город':
            get_sex(client_id)
            last_msg = 'пол'
        if msg == 'парня':
            sex = msg
            users_requests[client_id]['sex'] = 2
            get_age_from(client_id)
            last_msg = 'возраст от'
        if msg == 'девушку':
            sex = msg
            users_requests[client_id]['sex'] = 1
            get_age_from(client_id)
            last_msg = 'возраст от'
        elif last_msg == 'возраст от':
            try:
                age_f = int(msg.strip())
                users_requests[client_id]['age_from'] = age_f
                get_age_to(client_id)
                last_msg = 'возраст до'
            except ValueError:
                send_msg(client_id, 'Что-то пошло не так')
                get_age_from(client_id)
        elif last_msg == 'возраст до':
            try:
                age_t = int(msg.strip())
                users_requests[client_id]['age_to'] = age_t
                last_msg = 'минимум'
                confirm_data(id=client_id, city=city, sex=sex, age_from=age_f, age_to=age_t)
            except ValueError:
                send_msg(client_id, 'Что-то пошло не так')
                get_age_from(client_id)
        if msg == 'всё верно':
            send_msg(client_id, 'Работаем')
        if msg == 'изменить параметры':
            change_data(client_id)
        if msg == 'город':
            get_city(client_id)
            last_msg = 'меняем город'
        elif last_msg == 'меняем город':
            confirm_city(client_id, msg)
            last_msg = 'возраст до'



        print(users_requests)
        print(last_msg)
        print(msg)
