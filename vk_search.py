import requests
import time
from pprint import pprint
from auth_data import VK_TOKEN, v


def vk_users_search(params):
    api = 'https://api.vk.com/method/'
    method = 'users.search'
    url = api + method
    response = requests.get(url, params=params)

    return response.json()


def get_list(users_requests):
#    client_id = list(users_requests.keys())[0]
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
    count_matches = matches['response']['count']
    users_list = list()

    while offset <= count_matches:
        if offset != 0:
            matches = vk_users_search(params)
        for user in matches['response']['items']:
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
#            else:
#                aaa += 1
        offset += count
        params['offset'] = offset
        time.sleep(0.1)
#    print(aaa)
    return users_list


# us_list = get_list({18380222: {'city': 'скидель', 'sex': 1, 'age_from': 26, 'age_to': 26, 'token': ''}})
# print(len(us_list))
# print(us_list)