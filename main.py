from robot import flujo
from db_conn import start_db, consulta_por_keyword, consulta_por_url, consulta_urls, consulta_keys, create_keyword

from pydantic import BaseModel

from fastapi import FastAPI, Path
from fastapi.responses import FileResponse

app = FastAPI()

class Keyword(BaseModel):
    keyword: str
    url_id: int


@app.get('/')
def conection():
    start_db()
    return 'succes'


@app.get('/url/{consulta}/{id}', response_class=FileResponse)
def consulta_data_externa(consulta: str, id: int):
    url = consulta_por_url(id)
    ziped_file = flujo(consulta, url)
    return FileResponse(path=ziped_file, filename=ziped_file)


@app.get('/keyword/{id}', response_class=FileResponse)
def get_with_id_db(id: int):
    data = consulta_por_keyword(id)
    url = data[1]
    consulta = data[0]
    print(f'{consulta}, {url}')
    ziped_file = flujo(consulta, url)
    return FileResponse(path=ziped_file, filename=ziped_file)


@app.get('/url')
def get_url_list():
    urls = consulta_urls()
    return urls

@app.get('/keyword')
def get_keys_list():
    keys = consulta_keys()
    return keys

@app.post('/add-keyword')
def add_keyword(keywords: Keyword):
    added_keyword = keywords.keyword
    added_url = keywords.url_id
    create_keyword(added_keyword, added_url)        
    return f'keyword {keywords.keyword}añadido a la lista'
