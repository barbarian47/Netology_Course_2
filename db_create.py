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
        print(f"[INFO]=====>Connected PostgreSQL vk_user_list {cursor.fetchone()}")

    #Запросы на создание таблиц в БД
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE if not exists  list_user_param(    
            id_VK varchar(40) primary key,
            first_name varchar(40),
            last_name varchar(40));"""
        )
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE if not exists  list_links(
            id_links serial primary key,
            id_VK varchar(40) not null references list_user_param(id_VK),
            VK_link varchar(40) not null,
            link_photo varchar not null)"""
        )
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE if not exists  list_id(
                id_VK varchar(40) not null references list_user_param(id_VK),
                id_user_vk varchar(40) not null,
                in_black_list boolean,
                constraint id_vk_and_user_vk primary key (id_VK, id_user_vk));"""
        )
    
    
    
    
    
    


except Exception as _ex:
    print("[INFO] Error PostgreSQL", _ex)
finally:
    #разрываем коннект
    if connection:
        connection.close()
        print("[INFO]=====>PostgreSQL vk_user_list connection closed")
    