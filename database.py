import psycopg2

def connection():
    conn = psycopg2.connect(
        dbname = 'postgres',
        user = 'postgres',
        password = '0000',
        port = '5432',
        host = 'localhost'
    )
    return conn

def create_table():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                    id SERIAL PRIMARY KEY,
                    tg_id BIGINT UNIQUE,
                    name TEXT, 
                    phone TEXT, 
                    age INT)''')
    conn.commit()
    return cursor, conn

def save_info(tg_id, name, phone, age):
    cursor, conn = create_table()
    cursor.execute('''INSERT INTO orders (tg_id, name, phone, age)
                            VALUES (%s, %s, %s, %s) ON CONFLICT (tg_id) DO NOTHING''', [tg_id, name, phone, age])

    conn.commit()
