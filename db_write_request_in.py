import psycopg2
from config import host, user, password, db_name

# id_vk - id пользователя в VK
# vk_link - ссылка на профиль пользователя
# link_photo - список из 3-х ссылок на фотографии
# first_name - имя из профиля
# last_name - фамилия из профиля

user_info = {'partner_id': 392697333, 'link': 'vk.com/id392697334', 'first_name': 'Милана3', 
            'last_name': 'Вежель3',
            'photo': [
            (456239027, 'https://sun9-82.userapi.com/s/v1/if1/YDNet6DJyBVK-Mq4DL4AMv3XG2unU3L0OID9MCZVCXUxsPm2fP_-iA_hL0UeVcIx7L8Fosx-.jpg?size=640x640&quality=96&type=album'),
            (456239058, 'https://sun9-71.userapi.com/s/v1/if1/df2M0CT5JJDtL_xmvru7lUz1A1akw-xEdw0nbTFFKQGTA8o2TWv7ZL88q6XUuUCKSFdJv8KI.jpg?size=640x640&quality=96&type=album'),
            (456239028, 'https://sun9-63.userapi.com/s/v1/if1/EeSxOUhXOwqPTRuS0csrf5NHRzmKTtZE2jTod4N9iZVckUyTqf9Fv94JREEec_gIVQ6B0QKu.jpg?size=640x640&quality=96&type=album')
            ]
            }
id_client = 11111

def write_in_bd(id_client, user_info):
    id_client = id_client
    id_partner = user_info.get('partner_id')
    link = user_info.get('link')
    photo = user_info.get('photo')
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
            except:
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
        #разрываем коннект
        if connection:
            connection.close()
            print("[INFO]=====>PostgreSQL vk_user_list connection closed")
            return

def write_in_blacklist(client_id, user_id):
    id_client = client_id
    id_partner = user_id
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
            try:
                cursor.execute(
                    f"""INSERT INTO list_user_param(id_vk) VALUES
                        ({id_partner});"""
                )
            except:
                cursor.execute(
                    f"""INSERT INTO list_id(id_vk, id_user_vk, in_black_list) 
                    VALUES ({id_partner}, {id_client}, TRUE);"""
                )
                print("[INFO]PostgreSQL vk_user_list write write_list_id")
            else:
                cursor.execute(
                    f"""INSERT INTO list_id(id_vk, id_user_vk, in_black_list) 
                    VALUES ({id_partner}, {id_client}, TRUE);"""
                )
                print("[INFO]PostgreSQL write in black list")
    except Exception as _ex:
        print("[INFO] Error PostgreSQL", _ex)
    finally:
        #разрываем коннект
        if connection:
            connection.close()
            print("[INFO]=====>PostgreSQL vk_user_list connection closed")
            return


if __name__ == "__main__":
    write_in_bd(id_client, user_info)
    #write_in_blacklist(999999992, 888888884)