import psycopg2
from config import host, user, password, db_name

# id_vk - id пользователя в VK
# vk_link - ссылка на профиль пользователя
# link_photo - список из 3-х ссылок на фотографии
# first_name - имя из профиля
# last_name - фамилия из профиля

user_info = {'id_vk':'id308987349',
             'vk_link':'https://vk.com/id308987349',
             'link_photo':['https://vk.com/gim213360271?sel=18380222&z=photo-213360271_457239027%2Fmail866',
                         'https://vk.com/gim213360271?sel=18380222&z=photo-213360271_457239026%2Fmail866',
                          'https://vk.com/gim213360271?sel=18380222&z=photo-213360271_457239025%2Fmail866'],
             'first_name':'Лена',
             'last_name':'Петрова'}

def write_in_bd(user_info):
    id_vk = user_info.get('id_vk')
    vk_link = user_info.get('vk_link')
    link_photo = user_info.get('link_photo')
    first_name = user_info.get('first_name')
    last_name = user_info.get('last_name')

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
                f"""INSERT INTO list_id(id_vk) VALUES ('{id_vk}');
                    """
            )
            print("[INFO]PostgreSQL vk_user_list write write_list_id")

            cursor.execute(
                f"""INSERT INTO list_user_param(id_vk, first_name, last_name) VALUES
                    ('{id_vk}', '{first_name}', '{last_name}');"""
            )

            for iter in link_photo:
                with connection.cursor() as cursor:
                        cursor.execute(
                            f"""INSERT INTO list_links(id_vk, vk_link, link_photo) VALUES
                            ('{id_vk}', '{vk_link}', '{iter}');"""
                        )
                        print("[INFO]PostgreSQL vk_user_list write write_link_photo")
        
    except Exception as _ex:
        print("[INFO] Error PostgreSQL", _ex)
    finally:
        #разрываем коннект
        if connection:
            connection.close()
            print("[INFO]=====>PostgreSQL vk_user_list connection closed")
            return

if __name__ == "__main__":
    write_in_bd(user_info)