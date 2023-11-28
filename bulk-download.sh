#!/bin/bash
#
# Este script descarga todos los datasets de los portales de datos abiertos
# de la administración pública nacional Argentina.Para ejecutarlo, correr
# el siguiente comando:
#     bash bulk-download.sh
#
# Por cada portal, el script descarga el archivo data.json, lo procesa y genera
# un archivo zip con los datos y el data.json. El archivo zip se mueve luego guarda
# a la subcarpeta dumps.


download_dump() {
    local data_file_name="$2.data.json"
    echo "Downloading $1"
    wget -q $1
    if [ -f "data.json" ]; then
        mv data.json $data_file_name
        python from_data_json.py $data_file_name
        zip -r "dumps/$2.zip" "$2/" $data_file_name
        mv $data_file_name dumps/
        rm -r $2/
        echo "Downloaded $1"
    else
        echo "Cannot download $data_file_name. Skipping."
    fi
}


download_dump https://monitoreo.datos.gob.ar/catalog/jgm/data.json jgm
download_dump https://datosabiertos.enacom.gob.ar/data.json enacom
download_dump http://monitoreo.datos.gob.ar/catalog/otros/data.json otros
download_dump https://datos.arsat.com.ar/data.json arsat
download_dump https://monitoreo.datos.gob.ar/catalog/aaip/data.json aaip
download_dump https://monitoreo.datos.gob.ar/media/catalog/sedronar/data.json sedronar
download_dump https://monitoreo.datos.gob.ar/catalog/modernizacion/data.json modernizacion
download_dump https://monitoreo.datos.gob.ar/media/catalog/shn/data.json shn
download_dump https://monitoreo.datos.gob.ar/catalog/smn/data.json smn
download_dump https://monitoreo.datos.gob.ar/catalog/ign/data.json ign
download_dump http://datos.mindef.gov.ar/data.json mindef
download_dump https://monitoreo.datos.gob.ar/catalog/justicia/data.json justicia
download_dump https://monitoreo.datos.gob.ar/catalog/seguridad/data.json seguridad
download_dump https://datos.transporte.gob.ar/data.json transporte
download_dump https://monitoreo.datos.gob.ar/media/catalog/ambiente/data.json ambiente
download_dump http://datasets.datos.mincyt.gob.ar/data.json mincyt
download_dump https://datos.cultura.gob.ar/data.json cultura
download_dump https://datosabiertos.desarrollosocial.gob.ar/data.json desarrollo-social
download_dump http://andino.siu.edu.ar/data.json siu
download_dump https://monitoreo.datos.gob.ar/catalog/educacion/data.json educacion
download_dump https://datos.agroindustria.gob.ar/data.json agroindustria
download_dump http://datos.energia.gob.ar/data.json energia
download_dump https://monitoreo.datos.gob.ar/media/catalog/inti/data.json inti
download_dump https://monitoreo.datos.gob.ar/catalog/ssprys/data.json ssprys
download_dump https://www.presupuestoabierto.gob.ar/sici/rest-api/catalog/public presupuesto-abierto
download_dump https://datos.produccion.gob.ar/data.json produccion
download_dump https://infra.datos.gob.ar/catalog/sspm/data.json sspm
download_dump https://monitoreo.datos.gob.ar/catalog/ssprys/data.json ssprys
download_dump https://transparencia.enargas.gob.ar/data.json enargas
download_dump https://monitoreo.datos.gob.ar/catalog/siep/data.json siep
download_dump https://monitoreo.datos.gob.ar/catalog/exterior/data.json exterior
download_dump http://datos.pami.org.ar/data.json pami
download_dump http://datos.salud.gob.ar/data.json salud
download_dump https://monitoreo.datos.gob.ar/media/catalog/trabajo/data.json trabajo
download_dump http://datos.yvera.gob.ar/data.json yvera
download_dump https://datos.mininterior.gob.ar/data.json mininterior
download_dump https://monitoreo.datos.gob.ar/media/catalog/dine/data.json dine
download_dump https://monitoreo.datos.gob.ar/media/catalog/renaper/data.json renaper
download_dump https://monitoreo.datos.gob.ar/media/catalog/obras/data.json obras
download_dump http://datos.acumar.gob.ar/data.json acumar
download_dump https://monitoreo.datos.gob.ar/media/catalog/generos/data.json generos
