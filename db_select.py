"""Модль запросов в БД.
В модуле расзвернуты функции для получения данных из БД.
"""
import psycopg2
from config import host, user, password, db_name


def select_favorit_users_from_bd(client_id):
    """Функция получения списка избранных пользователей VK.
    :client_id - id VK пользователя,
    который запросил свой список избранных пользователей.
    :type - integer
    :return - словарь, в котором ключами являются
    id избранных пользователей(integer), а значениями список(list)
    параметров(str) избранного пользователя. Формат:
    {id_избранного_пользователя:
    ('Имя', 'Фамилия', 'ссылка на профиль VK')}
    :exception - ошибки обращения к БД.
    """
    try:
        favorit_users_list = []
        favorit_users_params = []
        favorit_users = {}
        #коннектимся к БД
        connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            database = db_name
        )
        connection.autocommit = True
        #Проверка коннекта к БД
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )
            print(f"[INFO]=====>Connected PostgreSQL vk_user_list {cursor.fetchone()}")
            cursor.execute(
                f"""SELECT id_vk FROM list_id
                WHERE id_user_vk = {client_id} AND in_black_list != TRUE;"""
            )
            raw_favorit_users_list = cursor.fetchall()
            for iter in range(len(raw_favorit_users_list)):
                favorit_users_list += raw_favorit_users_list[iter]
            for iter in favorit_users_list:
                cursor.execute(
                    f"""SELECT l_u.first_name, l_u.last_name, l_l.vk_link FROM list_user_param l_u
                    LEFT JOIN list_links l_l ON l_u.id_vk = l_l.id_vk
                    WHERE l_u.id_vk = {iter};"""
                )
                raw_favorit_users_params = cursor.fetchall()[0]
                favorit_users_params.append(raw_favorit_users_params)
            for iter in range(len(favorit_users_list)):
                new_key_value = {favorit_users_list[iter] : favorit_users_params[iter]}
                favorit_users.update(new_key_value)            
    except Exception as _ex:
        print("[INFO] Error PostgreSQL", _ex)
    finally:
        #разрываем коннект
        if connection:
            connection.close()
            print("[INFO]=====>PostgreSQL vk_user_list connection closed")
    return favorit_users


# возвращает id пользователей в виде set()
def select_blacklist(client_id):
    """Функция получения черного списка из БД.
    :client_id - id VK пользователя,
    который запрашивает свой черный список пользователей VK
    :type - integer
    :return - set() - список id пользователей(integer) в черном списке.
    Форма вывода:
    {id_пользователя1, id_пользователя2, ...}
    :exception - ошибки обращения к БД.
    """
    blacklist = []
    try:
        #коннектимся к БД
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        #Проверка коннекта к БД
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )
            print(f"[INFO]=====>Connected PostgreSQL vk_user_list {cursor.fetchone()}")
            cursor.execute(
                f"""SELECT id_VK FROM list_id
                WHERE in_black_list = true AND id_user_vk = {client_id};"""
            )
            raw_blacklist = cursor.fetchall()
            for iter in range(len(raw_blacklist)):
                blacklist += raw_blacklist[iter]
    except Exception as _ex:
        print("[INFO] Error PostgreSQL", _ex)
    finally:
        #разрываем коннект
        if connection:
            connection.close()
            print("[INFO]=====>PostgreSQL vk_user_list connection closed")
    return set(blacklist)


def all_clients():
    """Функция получения списка всех юзеров использующих бота.
    Функция не принимает аргументов.
    :return - set() - список id пользователей(integer)
    которые использовали бот и оставили записи в БД.
    Форма вывода:
    {id_пользователя1, id_пользователя2, ...}
    :exception - ошибки обращения к БД.
    """
    all_clients = set()
    try:
        #коннектимся к БД
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        #Проверка коннекта к БД
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )
            print(f"[INFO]=====>Connected PostgreSQL vk_user_list {cursor.fetchone()}")
            cursor.execute(
                f"""SELECT DISTINCT id_user_vk FROM list_id;"""
            )
            raw_all_clients = cursor.fetchall()
            for iter in raw_all_clients:
                all_clients.add(iter[0])
    except Exception as _ex:
        print("[INFO] Error PostgreSQL", _ex)
    finally:
        #разрываем коннект
        if connection:
            connection.close()
            print("[INFO]=====>PostgreSQL vk_user_list connection closed")
    return all_clients


def select_count(id_client):
    pass
