import psycopg2
from psycopg2 import Error

try:
    print("Подключение к PostgreSQL...")
    conn = psycopg2.connect("""
        host=localhost
        port=5432
        dbname=auth_service_db
        user=server
        password='password'
        target_session_attrs=read-write
    """)

    cursor = conn.cursor()
    cursor.execute('SELECT version()')
    # cursor.execute('DROP TABLE IF EXISTS users CASCADE;')
    # conn.commit()

    # cursor.execute('SELECT * from users')
    # request1 = cursor.fetchone()
    print(cursor.fetchone())
    # cursor.execute("""
    #                 SELECT *
    #                 FROM data_raw LIMIT 100
    #                """)
    # request1 = cursor.fetchall()
    # print(request1)
    

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)

finally:
    if conn:
        cursor.close()
        conn.close()
        print("Соединение с PostgreSQL закрыто")