from pprint import pprint
from vk_search import get_list
from vk_get_photo import create_top_photo_list
from auth_data import VK_TOKEN


def vk_match(client_id, users_requests):
    match_list = {client_id: []}
    hometown = users_requests[client_id]['city'].title()
    sex = users_requests[client_id]['sex']
    age_from = users_requests[client_id]['age_from']
    age_to = users_requests[client_id]['age_to']
    if users_requests[client_id]['token']:
        token = users_requests[client_id]['token']
    else:
        token = VK_TOKEN

    try:
        users_list = get_list(hometown=hometown, sex=sex, age_from=age_from, age_to=age_to, token=token)
    except KeyError:
        return 'Ошибка'

    for user in users_list:
#        print(user)
        photo_data = create_top_photo_list(id=user['id'], token=token)
        user_data = {
                'partner_id': user['id'],
                'link': 'vk.com/' + user['domain'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'photo': []
        }
        for photo in photo_data:
            user_data['photo'].append(photo['url'])

        match_list[client_id].append(user_data)

    return match_list



# pprint(vk_match(18380222, {18380222: {'city': 'гродно', 'sex': 1, 'age_from': 31, 'age_to': 33, 'token': ''}}))