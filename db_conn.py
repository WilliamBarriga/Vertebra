import sqlite3

def start_db():
    try:
        connection = sqlite3.connect('testingdb.db', check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS urls(id integer PRIMARY KEY autoincrement, url text UNIQUE, enable boolean NOT NULL)')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS keywords(id integer PRIMARY KEY autoincrement, keyword text, id_url integer NOT NULL, foreign key(id_url) REFERENCES urls(id))')
        cursor.execute(
            'INSERT INTO urls(id, url, enable) VALUES (?, ?, ?)', (1, "https://www.datos.gov.co/", True))
        cursor.execute(
            'INSERT INTO keywords(keyword, id_url) VALUES (?, ?)', ("datos", 1))
        cursor.execute(
            'INSERT INTO keywords(keyword, id_url) VALUES (?, ?)', ("icetex", 1))
        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        cursor.close()
        connection.close()
        print(f'a ocurrido el error: {e}')


def consulta_por_keyword(id):
    connection = sqlite3.connect('testingdb.db', check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    result = cursor.execute(f'SELECT * FROM keywords WHERE id={id}').fetchone()
    keywords = result['keyword']
    url_foreign = result['id_url']
    url = consulta_por_url(url_foreign)
    cursor.close()
    connection.close()
    return keywords, url

def consulta_por_url(id):
        connection = sqlite3.connect('testingdb.db', check_same_thread=False)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        result = cursor.execute(f'SELECT url FROM urls WHERE id={id}').fetchone()
        url = str(result['url'])
        cursor.close()
        connection.close()
        return url


def consulta_urls():
    connection = sqlite3.connect('testingdb.db', check_same_thread=False)
    #connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    result = cursor.execute(f'SELECT id, url FROM urls').fetchall()
    cursor.close()
    connection.close()
    return result

def consulta_keys():
    connection = sqlite3.connect('testingdb.db', check_same_thread=False)
    #connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    result = cursor.execute(f'SELECT id, keyword, id_url FROM keywords').fetchall()
    cursor.close()
    connection.close()
    return result

def create_keyword(keyword, id_url):
    connection = sqlite3.connect('testingdb.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO keywords(keyword, id_url) VALUES (?, ?)', (keyword, id_url))
    connection.commit()
    cursor.close()
    connection.close()
