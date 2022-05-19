import requests
from pprint import pprint
from auth_data import VK_USER_ID, VK_TOKEN, v


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


def create_top_photo_list(id, token=VK_TOKEN):
    photos_data = vk_photo_data(id, token=token)
    count_photo = photos_data['response']['count']
    offset = 0
    count = 50
    photo_list = list()
    top_1 = 0
    top_2 = 0
    top_3 = 0
    while offset <= count_photo:
        if offset != 0:
            photos_data = vk_photo_data(id=id, offset=offset, token=token)
        for photo in photos_data['response']['items']:
            if photo['likes']['count'] > top_1:
                if len(photo_list) == 3:
                    photo_list.pop()
                top_3 = top_2
                top_2 = top_1
                top_1 = photo['likes']['count']
                photo_info = {photo['id']: top_1, 'url': photo['sizes'][-1]['url']}
                photo_list.insert(0, photo_info)
            elif photo['likes']['count'] > top_2:
                if len(photo_list) == 3:
                    photo_list.pop()
                top_3 = top_2
                top_2 = photo['likes']['count']
                photo_info = {photo['id']: top_2, 'url': photo['sizes'][-1]['url']}
                photo_list.insert(1, photo_info)
            elif photo['likes']['count'] > top_3:
                if len(photo_list) == 3:
                    photo_list.pop()
                top_3 = photo['likes']['count']
                photo_info = {photo['id']: top_3, 'url': photo['sizes'][-1]['url']}
                photo_list.append(photo_info)
        offset += count

    return photo_list


pprint(create_top_photo_list(id=151127943))
#pprint(vk_photo_data(id=151127943))