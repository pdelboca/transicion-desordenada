# Transicion Desordenada

Backup ciudadano de datos públicos.

Este repositorio contiene código que permite descargar todos los archivos de diversos portales de datos de la República Argentina.

## Uso

`from_data_json.py` descarga en una carpeta los archivos de un portal cuyo `data.json` haya sido pasado por parametro. La carpeta tiene el nombre del identificador del portal (`acumar`, `Agro`, `energia`, etc)

Ejemplo:

```bash
# descarga en energia/
python from_data_json.py energia.data.json

# descarga en acumar/
python from_data_json.py acumar.data.json

# descarga en yvera/
python from_data_json.py yvera.data.json

```