from turtle import update
import psycopg2
from config import host, user, password, db_name


def select_favorit_users_from_bd(client_id):
    try:
        favorit_users_list =[]
        favorit_users_params = []
        favorit_users ={}
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
                f"""SELECT id_vk FROM list_id
                WHERE id_user_vk = {client_id};"""
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
                WHERE in_black_list = true AND id_user_vk = {client_id};
                    """
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



if __name__ == "__main__":
    print(select_favorit_users_from_bd(11111))
    #print(select_blacklist(999999990))