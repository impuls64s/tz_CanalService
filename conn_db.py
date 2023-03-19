import time
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    try:
        conn = psycopg2.connect(
            database = os.environ.get('POSTGRES_DB'),
            user = os.environ.get('POSTGRES_USER'),
            password = os.environ.get('POSTGRES_PASSWORD'),
            host = os.environ.get("P_HOST", "localhost")
    )
    except psycopg2.OperationalError as error:
        print(f'[-] БД еще не готова! Повторное подключение через 3 сек.')
        time.sleep(3)
        main()
    except (Exception, psycopg2.Error) as error:
        raise error
    else:
        conn.close()


if __name__ == "__main__":
    main()
