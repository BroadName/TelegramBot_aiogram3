import psycopg2
from psycopg2 import Error
import configparser


config = configparser.ConfigParser()
config.read('db_config.ini')

user = config['params']['user']
password = config['params']['password']
host = config['params']['host']
port = config['params']['port']


def create_db():
    try:
        connection = psycopg2.connect(user=user, password=password, host=host, port=port)
        sql_create_database = f'CREATE DATABASE learn_english_db'
        cursor = connection.cursor()
        connection.autocommit = True
        cursor.execute(sql_create_database)
        cursor.close()
        connection.close()
    except (Exception, Error) as e:
        print('Error is occurred: ', e)


create_db()


def create_tables():
    try:
        with psycopg2.connect(user=user, password=password, host=host, port=port, database='learn_english_db') as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                sql_create_table = '''CREATE TABLE IF NOT EXISTS user_data (
                                        user_id BIGINT PRIMARY KEY,
                                        user_name VARCHAR(100) NOT NULL);
                                    '''
                cur.execute(sql_create_table)
                sql_create_table = '''CREATE TABLE IF NOT EXISTS word (
                                        word_id SERIAL PRIMARY KEY,
                                        english VARCHAR(100) NOT NULL,
                                        translate VARCHAR(100) NOT NULL);
                                    '''
                cur.execute(sql_create_table)
                sql_create_table = '''CREATE TABLE IF NOT EXISTS users_word (
                                        u_w_id SERIAL PRIMARY KEY,
                                        word_id INT NOT NULL,
                                        user_id BIGINT NOT NULL,
                                        CONSTRAINT fk_user_data FOREIGN KEY(user_id) 
                                            REFERENCES user_data(user_id) ON DELETE CASCADE,
                                        CONSTRAINT fk_word FOREIGN KEY(word_id)
                                            REFERENCES word(word_id) ON DELETE CASCADE);
                                        '''
                cur.execute(sql_create_table)
                print('Yours tables was created!')
    except (Exception, Error) as e:
        print('Error is occurred: ', e)


create_tables()
