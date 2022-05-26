import requests
import time
from auth_data import VK_TOKEN, v
from db_select import select_blacklist


def vk_users_search(params):
    """
    Функция делает запрос через API ВКонтактке

    :param params: параметры запроса
    :type params: dict

    :return response: json с ответом от API
    :type response: dict
    """
    api = 'https://api.vk.com/method/'
    method = 'users.search'
    url = api + method
    response = requests.get(url, params=params)

    return response.json()


def get_list(id, users_requests):
    """
    Функция ищет пользователей подходящих под заданные параметры

    :param id: id клиента сформировавшего запрос
    :type id: int
    :param users_requests: словарь с параметрами запроса
    :type users_requests: dict

    :return users_list: список словарей с подходящими пользователями
    :type users_list: list

    :exception KeyError: не корректный токен доступа
    """
    hometown = users_requests['city'].title()
    sex = users_requests['sex']
    age_from = users_requests['age_from']
    age_to = users_requests['age_to']
    if users_requests['token']:
        token = users_requests['token']
    else:
        token = VK_TOKEN

    offset = 0
    count = 1000
    fields = 'domain, music, books, interests, movies, relation'
    fields_list = [i for i in fields.split(', ')]
    params = {
        'access_token': token,
        'v': v,
        'sex': sex,
        'hometown': hometown.title(),
        'age_from': age_from,
        'age_to': age_to,
        'offset': offset,
        'count': count,
        'fields': fields
    }
    matches = vk_users_search(params)
    try:
        count_matches = matches['response']['count']
    except KeyError:
        return 'Ошибка токена'
    users_list = list()

    # Получаем чёрный список пользователя
    black_list = select_blacklist(id)

    while offset <= count_matches:
        if offset != 0:
            matches = vk_users_search(params)
        for user in matches['response']['items']:
            if user['id'] not in black_list:
                if user['can_access_closed']:
                    data = dict()
                    data['id'] = user['id']
                    data['first_name'] = user['first_name']
                    data['last_name'] = user['last_name']
                    data['domain'] = user['domain']
                    for field in fields_list:
                        if field in user and user[field]:
                            data[field] = user[field]
                    users_list.append(data)

        offset += count
        params['offset'] = offset
        time.sleep(0.1)

    return users_list


def client_info(id):
    """
    Функция получает данные собеседника

    :param id: id собеседника
    :type id: int

    :return response: json с информацией о собеседнике
    :type response: dict
    """
    api = 'https://api.vk.com/method/'
    method = 'users.get'
    url = api + method
    params = {
        'access_token': VK_TOKEN,
        'v': v,
        'user_ids': id
    }
    response = requests.get(url, params=params)

    return response.json()
