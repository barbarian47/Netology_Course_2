"""Модуль создания таблиц и связей в БД.
Перед запуском модуля необходимо создать БД PostgreSQL.

В файл config.py необходимо поместить следующие данные для подключения к созданной БД:
host = "127.0.0.1" - для локально развернутой БД
user = "" - имя пользователя БД.
password = "" - пароль доступа к БД.
db_name = "" - название БД.

После запуска скрипт сформирует таблицы и взаимосвязи в БД.
В консоль принтами выведены события создания и разрыва коннектора с БД.
"""

import psycopg2
from config import host, user, password, db_name


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
        print(
            f"[INFO]=====>Connected PostgreSQL vk_user_list {cursor.fetchone()}")

        cursor.execute(
            """CREATE TABLE if not exists  list_user_param(    
                id_VK integer primary key,
                first_name varchar(40),
                last_name varchar(40));"""
        )

        cursor.execute(
            """CREATE TABLE if not exists  list_links(
                id_links serial primary key,
                id_VK integer not null references list_user_param(id_VK),
                VK_link varchar(40) not null,
                link_photo varchar not null,
                id_photo integer not null);"""
        )

        cursor.execute(
            """CREATE TABLE if not exists  list_id(
                    id_VK integer not null references list_user_param(id_VK),
                    id_user_vk integer not null,
                    in_black_list boolean,
                    constraint id_vk_and_user_vk primary key (id_VK, id_user_vk));"""
        )
        cursor.execute(
            """CREATE TABLE if not exists  id_client_sesion(
                    id_session serial primary key,
                    id_client integer not null,
                    count integer not null,
                    params json not null);"""
        )
except Exception as _ex:
    print("[INFO] Error PostgreSQL", _ex)
finally:
    #разрываем коннект
    if connection:
        connection.close()
        print("[INFO]=====>PostgreSQL vk_user_list connection closed")
