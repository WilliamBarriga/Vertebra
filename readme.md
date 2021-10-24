# Vertebra API Selenium FastAPI

_Robot automatizado para la descarga de informacion de la pagina https://datos.go.co/_

## Pre-requisitos

- Descargar  de  https://www.selenium.dev/downloads/  Selenium Server Grid (para el desarrollo del API se uso la version 4.0.0).
- Descargar de https://chromedriver.chromium.org/downloads el WebDriver necesario para el uso de Selenium (Para el desarrollo del API se uso la version 95.0.4638.17)

- Guardar los archivos descargados en la raiz del proyecto_

- Instalar dependecias necesarias de Python:
```
pip install -r requirements.txt
```

## Instalación
_En la raiz del proyecto ejecutar los siguientes comandos:_


- Poner en marcha el servidor de Selenium:
```
java -jar selenium-server-4.0.0.jar standalone --host 127.0.0.1
```

- Iniciar servidor de uvicorn para la ejecucion de FastAPI:
```
uvicorn main:app --reload
```
o en caso de que no se reconozca el comando se puede usar:
```
python -m uvicorn main:app --reload
```


## Endpoints configurados

### - (/)
- Solicitud tipo GET que crea y verifica la conexion a la DB SQLite configurada

### - (/url)
- Solicitud tipo GET que devuelve una lista con los urls que hay en la DB (no se pueden añadir mas)

### -(/keyword)
- Solicitud tipo GET que devuelve una lista con las keyword de busqueda que hay en la DB

### -(/add-keyword)
- solicitud tipo POST que recibe como parametros del BODY una keyword y el url_id al que va asociado la keyword
```
{
  "keyword": "string",
  "url_id": 0
}
```

### -(/ulr/{consulta}/{url})
- Solicitud tipo Get que recibe como parametro la palabra a consultar y el id de un url guardado en la DB, genera como resultado un archivo .zip con los archivos .csv y el reporte .txt de los mismos.
> http://localhost/url/icetex/1
> http://lovalhost/url/ambiente/1

### -(/keyword/{id})
- Solicitud tipo Get que recibe como paratametro el id de la keyword que se quiere utilizar alojada en la DB, genera como resultado un archivo .zip con los archivos .csv y el reporte .txt de los mismos.
> http://localhost/keyword/1
> http://localhost/keyword/3
