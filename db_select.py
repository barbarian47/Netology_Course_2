import psycopg2
from config import host, user, password, db_name


def select_favorit_users_from_bd(client_id):
    try:
        favorit_users_list =[]
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
    except Exception as _ex:
        print("[INFO] Error PostgreSQL", _ex)
    finally:
        #разрываем коннект
        if connection:
            connection.close()
            print("[INFO]=====>PostgreSQL vk_user_list connection closed")
    return favorit_users_list

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
    print(select_favorit_users_from_bd(100000000))
    #print(select_blacklist(999999990))