import psycopg2
from config import host, user, password, db_name

def selec_favorit_users_from_bd():
    favorit_users_list =[]

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
                f"""SELECT DISTINCT vk_link FROM list_links;
                    """
            )
            favorit_users_list = cursor.fetchone()   
    except Exception as _ex:
        print("[INFO] Error PostgreSQL", _ex)
    finally:
        #разрываем коннект
        if connection:
            connection.close()
            print("[INFO]=====>PostgreSQL vk_user_list connection closed")
    return favorit_users_list

if __name__ == "__main__":
    print(selec_favorit_users_from_bd())