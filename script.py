import psycopg2
from rate_cbr import usd_exchange_rate
from sheets_get_values import get_values
import time
from dotenv import load_dotenv
import os


load_dotenv()

def update_db(table_google):

    try:
        conn = psycopg2.connect(
            database = os.getenv('DB_NAME'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            host = os.getenv('DB_HOST'),
            port = os.getenv('DB_PORT')
        )
        cur = conn.cursor()
        cur.execute(
            "SELECT id, order_id, price_dollars, delivery_time FROM first_app_firstapp;"
        )
        table_db = cur.fetchall()
        
        # Находим данные которые нужно добавить или изменить
        add_or_update = list(set(table_google) - set(table_db))
        
        # Находим данные которые нужно изменить или удалить
        update_or_delete = list(set(table_db) - set(table_google))

        # Данные для обновления полученые путем нахождениях общих order_id
        update_data = tuple(
            filter(
                lambda x : x[1] in (order[1] for order in update_or_delete),
                add_or_update
            )
        )
    
        # Новые данные для вставки в таблицу, 
        # которые есть в гугл таблице, но нет в БД
        insert_data = tuple(
            filter(
                lambda x : x[1] not in (order[1] for order in update_or_delete),
                add_or_update
            )
        )

        # Данные которых нет в Google таблице и которые мы удалим из БД
        delete_data = tuple(
            filter(
                lambda x : x[1] not in (order[1] for order in add_or_update),
                update_or_delete
            )
        )

        print('[+] Внесение изменений в БД: '
              'Добавлено: {} | Обновлено: {} | Удалено: {} записи.'
              .format(len(insert_data), len(update_data), len(delete_data))
        )
        
        if insert_data:
            for item in insert_data:
                cur.execute(
                    "INSERT INTO first_app_firstapp VALUES (%s, %s, %s, %s, %s);",
                    (
                        item[0],
                        item[1],
                        item[2],
                        usd_exchange_rate(int(item[2])),
                        item[3]
                    )
                )
            conn.commit()

        if update_data:
            for item in update_data:
                cur.execute(
                    """UPDATE first_app_firstapp SET 
                        id = %s,
                        price_dollars = %s,
                        price_rubles = %s,
                        delivery_time = %s
                        WHERE order_id = %s;
                    """,
                    (
                        item[0],
                        item[2],
                        usd_exchange_rate(int(item[2])),
                        item[3],
                        item[1],
                    )
                )
            conn.commit()

        if delete_data:
            for item in delete_data:
                cur.execute(
                    "DELETE FROM first_app_firstapp WHERE order_id=%s",
                    [item[1]]
                )
                conn.commit()


    except Exception as ex:
        print(ex)
 
    finally:
        cur.close()
        conn.close()
    

def main(timeout=1):

    with open('last_data.txt', 'r') as file:
        last_data = file.read()

    while True:
        try:
            new_values = get_values()
            
            if last_data == str(new_values):
                print('[INFO] Данные в Google таблице не изменились.')
            else:
                print('[+] Google таблица изменилась, обновляю БД')
                last_data = str(new_values)
                update_db(new_values)

            time.sleep(timeout)
    
        except KeyboardInterrupt:
            print('\nСкрипт остановлен. Пока!')
            break
        
        finally:
            with open('last_data.txt', 'w') as file:
                file.write(last_data)


if __name__ == '__main__':
    main()
