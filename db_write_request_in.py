"""Модль запросов в БД.
В модуле расзвернуты функции для записи данных в БД.
"""
import psycopg2
from config import host, user, password, db_name


def write_in_bd(id_client, user_info):
    """Функция записи в БД понравившегося пользователя VK.
    :id_client - id VK пользователя,
    который направил запрос на зпись данных в БД.
    :type - integer
    :user_info - словарь с данными о записываемом пользователе.
    :type - dict
    Форма user_info:
    user_info = {'partner_id': type - integer, 'link': type - str, 'first_name': type - str,
            'last_name': type - str,
            'photo': [link_1, link_2, link_3
            ]}
            :partner_id - id пользователя VK которого надо записать в БД как понравившегося.
            :link - ссылка на профиль понравившегося пользователя.
            :first_name - имя из профиля
            :last_name - фамилия из профиля
            :link_photo - список из 3-х ссылок на фотографии понравившегося пользователя.
            Отбор фото осуществляется по максимальному количеству лайков.
    :exception - ошибки обращения к БД.
    """
    id_client = id_client
    id_partner = user_info.get('partner_id')
    link = user_info.get('link')
    photo = user_info.get('photo')
    first_name = user_info.get('first_name')
    last_name = user_info.get('last_name')
    try:
        # коннектимся к БД
        connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            database = db_name
        )
        connection.autocommit = True
        # Проверка коннекта к БД
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )
            print(
                f"[INFO]=====>Connected PostgreSQL vk_user_list {cursor.fetchone()}")
            try:
                cursor.execute(
                    f"""INSERT INTO list_user_param(id_vk, first_name, last_name) VALUES
                        ({id_partner}, '{first_name}', '{last_name}');"""
                )
                for iter in photo:
                    cursor.execute(
                        f"""INSERT INTO list_links(id_vk, vk_link, id_photo, link_photo) VALUES
                                ({id_partner}, '{link}', {iter[0]}, '{iter[1]})');"""
                    )
                    print("[INFO]PostgreSQL vk_user_list write write_link_photo")
            except Exception as _ex:
                cursor.execute(
                    f"""INSERT INTO list_id(id_vk, id_user_vk, in_black_list) 
                    VALUES ({id_partner}, {id_client}, FALSE);"""
                )
                print("[INFO]PostgreSQL vk_user_list write write_list_id")
            else:
                cursor.execute(
                    f"""INSERT INTO list_id(id_vk, id_user_vk, in_black_list) 
                    VALUES ({id_partner}, {id_client}, FALSE);"""
                )
                print("[INFO]PostgreSQL vk_user_list write write_list_id")
    except Exception as _ex:
        print("[INFO] Error PostgreSQL", _ex)
    finally:
        # разрываем коннект
        if connection:
            connection.close()
            print("[INFO]=====>PostgreSQL vk_user_list connection closed")
            return


def write_in_blacklist(id_client, id_partner):
    """Функция записи в БД пользователя,
    которого необходимо поместить в черный список
    :id_client - id VK пользователя,
    который направил запрос на зпись данных в БД.
    :type - integer
    :id_partner - id пользователя VK которого надо записать в БД как понравившегося.
    :type - integer
    :exception - ошибки обращения к БД.
    """
    try:
        # коннектимся к БД
        connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            database = db_name
        )
        connection.autocommit = True
        # Проверка коннекта к БД
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )
            print(
                f"[INFO]=====>Connected PostgreSQL vk_user_list {cursor.fetchone()}")
            try:
                cursor.execute(
                    f"""INSERT INTO list_user_param(id_vk) 
                    VALUES ({id_partner});"""
                )
                cursor.execute(
                    f"""INSERT INTO list_id(id_vk, id_user_vk, in_black_list) 
                    VALUES ({id_partner}, {id_client}, TRUE);"""
                )
                print("[INFO]PostgreSQL vk_user_list write write_list_id")
            except Exception as _ex:
                cursor.execute(
                    f"""UPDATE list_id
                    SET in_black_list = TRUE
                    WHERE id_vk = {id_partner} AND id_user_vk = {id_client};"""
                )
                print("[INFO]PostgreSQL vk_user_list write write_list_id")
    except Exception as _ex:
        print("[INFO] Error PostgreSQL", _ex)
    finally:
        # разрываем коннект
        if connection:
            connection.close()
            print("[INFO]=====>PostgreSQL vk_user_list connection closed")
            return


def write_count(id_client, count, params):
    """Функция счетчика.
    Функция записывает в БД счетчик обращений к боту.
    :id_client - id VK пользователя, который обращается к боту.
    :type - integer
    :count - счетчик
    :type - integer
    :param - параметры запроса в формате:
    {"city": "", "sex": , "age_from": , "age_to": , "token": ""}
    :type - json
    """   
    try:
        # коннектимся к БД
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        # Проверка коннекта к БД
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )
            print(
                f"[INFO]=====>Connected PostgreSQL vk_user_list {cursor.fetchone()}")
            try:
                cursor.execute(
                    f"""INSERT INTO id_client_sesion(id_client, _count, params) 
                    VALUES({id_client}, {count}, '{params}');;"""
                )
            except Exception as _ex:
                cursor.execute(
                    f"""UPDATE id_client_sesion
                    SET _count = {count}, params = '{params}'
                    WHERE id_client = {id_client};"""
                )
                print("[INFO]PostgreSQL vk_user_list write write_list_id")
    except Exception as _ex:
        print("[INFO] Error PostgreSQL", _ex)
    finally:
        # разрываем коннект
        if connection:
            connection.close()
            print("[INFO]=====>PostgreSQL vk_user_list connection closed")
            return

if __name__ == "__main__":
    write_count(18380222, 2, '{"city": "скидель", "sex": 1, "age_from": 30, "age_to": 28, "token": ""}')