import requests
import time
from pprint import pprint
from auth_data import VK_TOKEN, v


def vk_photo_data(id, offset=0, count=50, token=VK_TOKEN):
    api = 'https://api.vk.com/method/photos.getAll'
    params = {
        'owner_id': id,
        'access_token': token,
        'offset': offset,
        'count': count,
        'extended': True,
        'v': v
    }
    response = requests.get(api, params)

    return response.json()


def create_top_photo_list(user, token=VK_TOKEN):
    id = user['id']
    photos_data = vk_photo_data(id, token=token)
    count_photo = photos_data['response']['count']
    offset = 0
    count = 50
    photo_list = list()
    top_1 = 0
    top_2 = 0
    top_3 = 0
    while offset <= count_photo:
        time.sleep(0.15)
        if offset != 0:
            photos_data = vk_photo_data(id=id, offset=offset, token=token)
        for photo in photos_data['response']['items']:
            if photo['likes']['count'] > top_1:
                if len(photo_list) == 3:
                    photo_list.pop()
                top_3 = top_2
                top_2 = top_1
                top_1 = photo['likes']['count']
                photo_info = (photo['id'], photo['sizes'][-1]['url'])
                photo_list.insert(0, photo_info)
            elif photo['likes']['count'] > top_2:
                if len(photo_list) == 3:
                    photo_list.pop()
                top_3 = top_2
                top_2 = photo['likes']['count']
                photo_info = (photo['id'], photo['sizes'][-1]['url'])
                photo_list.insert(1, photo_info)
            elif photo['likes']['count'] > top_3:
                if len(photo_list) == 3:
                    photo_list.pop()
                top_3 = photo['likes']['count']
                photo_info = (photo['id'], photo['sizes'][-1]['url'])
                photo_list.append(photo_info)
        offset += count

    user_data = {
        'partner_id': user['id'],
        'link': 'vk.com/' + user['domain'],
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'photo': photo_list
    }

    return user_data


#pprint(create_top_photo_list({'id': 54463067, 'first_name': 'Инна', 'last_name': 'Польгуй', 'domain': 'id54463067'}))