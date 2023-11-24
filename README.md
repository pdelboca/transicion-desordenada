# Transicion Desordenada

Backup ciudadano de datos públicos.

Este repositorio contiene código que permite descargar todos los archivos de diversos portales de datos de la República Argentina.

## Descargar usando el data.json del portal (DCAT)

`from_data_json.py` descarga en una carpeta los archivos de un portal cuyo `data.json` haya sido pasado por parametro. La carpeta tiene el nombre del identificador del portal (`acumar`, `Agro`, `energia`, etc)

Ejemplo:

```bash
# descarga en energia/
python from_data_json.py energia.data.json

# descarga en acumar/
python from_data_json.py acumar.data.json
```

#### Listado de portales con data.json

 - https://datos.gob.ar/data.json
 - https://datos.acumar.gov.ar/data.json
 - https://datos.yvera.gob.ar/data.json
 - https://datos.mindef.gov.ar/data.json
 - https://datos.energia.gob.ar/data.json
 - https://datosabiertos.chaco.gob.ar/data.json
 - https://datos.santafe.gob.ar/data.json

## Ejemplo de descargas

Acá hay dos portales que se pueden descargar para mirar el resultado final:

 - Datos Abiertos de Turismo [123 MB](https://drive.google.com/file/d/1sijGeoNY629mXjksgltMAvAxMD41zqHQ/view?usp=sharing)
 - Autoridad de Cuenca Matanza Riachuelo [1.4 GB](https://drive.google.com/file/d/1jlyf4m6NaMVhJI360mBcZt9DZaH9ODuc/view?usp=sharing)
