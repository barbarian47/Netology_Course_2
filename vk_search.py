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


def get_list(hometown, sex, age_from=None, age_to=None, token=VK_TOKEN):
    offset = 0
    count = 1000
    fields = 'domain, music, books, interests, movies, relation'
    fields_list = [i for i in fields.split(', ')]
    params = {
        'access_token': token,
        'v': v,
        'sex': sex,
        'hometown': hometown,
        'age_from': age_from,
        'age_to': age_to,
        'offset': offset,
        'count': count,
        'fields': fields
    }
    matches = vk_users_search(params)
    count_matches = matches['response']['count']
#    print(count_matches)
    users_list = list()
#    aaa = 0
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
        time.sleep(0.5)
#    print(aaa)
    return users_list


us_list = get_list(hometown='Гродно', sex=1, age_from=25, age_to=30)
print(len(us_list))
pprint(us_list)