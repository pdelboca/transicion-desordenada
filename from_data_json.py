import json
import logging
import multiprocessing
import os
import requests
import shutil
import zipfile

logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

_PORTALS = [
    ('https://monitoreo.datos.gob.ar/catalog/jgm/data.json', 'jgm'),
    ('https://datosabiertos.enacom.gob.ar/data.json', 'enacom'),
    ('https://monitoreo.datos.gob.ar/catalog/otros/data.json', 'otros'),
    ('https://datos.arsat.com.ar/data.json', 'arsat'),
    ('https://monitoreo.datos.gob.ar/catalog/aaip/data.json', 'aaip'),
    ('https://monitoreo.datos.gob.ar/media/catalog/sedronar/data.json', 'sedronar'),
    ('https://monitoreo.datos.gob.ar/catalog/modernizacion/data.json', 'modernizacion'),
    ('https://monitoreo.datos.gob.ar/media/catalog/shn/data.json', 'shn'),
    ('https://monitoreo.datos.gob.ar/catalog/smn/data.json', 'smn'),
    ('https://monitoreo.datos.gob.ar/catalog/ign/data.json', 'ign'),
    ('http://datos.mindef.gov.ar/data.json', 'mindef'),
    ('https://monitoreo.datos.gob.ar/catalog/justicia/data.json', 'justicia'),
    ('https://monitoreo.datos.gob.ar/catalog/seguridad/data.json', 'seguridad'),
    ('https://datos.transporte.gob.ar/data.json', 'transporte'),
    ('https://monitoreo.datos.gob.ar/media/catalog/ambiente/data.json', 'ambiente'),
    ('https://datasets.datos.mincyt.gob.ar/data.json', 'mincyt'),
    ('https://datos.cultura.gob.ar/data.json', 'cultura'),
    ('https://datosabiertos.desarrollosocial.gob.ar/data.json', 'desarrollo-social'),
    ('http://andino.siu.edu.ar/data.json', 'siu'),
    ('https://monitoreo.datos.gob.ar/catalog/educacion/data.json', 'educacion'),
    ('https://datos.agroindustria.gob.ar/data.json', 'agroindustria'),
    ('http://datos.energia.gob.ar/data.json', 'energia'),
    ('https://monitoreo.datos.gob.ar/media/catalog/inti/data.json', 'inti'),
    ('https://monitoreo.datos.gob.ar/catalog/ssprys/data.json', 'ssprys'),
    ('https://www.presupuestoabierto.gob.ar/sici/rest-api/catalog/public', 'presupuesto-abierto'),
    ('https://datos.produccion.gob.ar/data.json', 'produccion'),
    ('https://infra.datos.gob.ar/catalog/sspm/data.json', 'sspm'),
    ('https://monitoreo.datos.gob.ar/catalog/ssprys/data.json', 'ssprys'),
    ('https://transparencia.enargas.gob.ar/data.json', 'enargas'),
    ('https://monitoreo.datos.gob.ar/catalog/siep/data.json', 'siep'),
    ('https://monitoreo.datos.gob.ar/catalog/exterior/data.json', 'exterior'),
    ('http://datos.pami.org.ar/data.json', 'pami'),
    ('http://datos.salud.gob.ar/data.json', 'salud'),
    ('https://monitoreo.datos.gob.ar/media/catalog/trabajo/data.json', 'trabajo'),
    ('http://datos.yvera.gob.ar/data.json', 'yvera'),
    ('https://datos.mininterior.gob.ar/data.json', 'mininterior'),
    ('https://monitoreo.datos.gob.ar/media/catalog/dine/data.json', 'dine'),
    ('https://monitoreo.datos.gob.ar/media/catalog/renaper/data.json', 'renaper'),
    ('https://monitoreo.datos.gob.ar/media/catalog/obras/data.json', 'obras'),
    ('http://datos.acumar.gob.ar/data.json', 'acumar'),
    ('https://monitoreo.datos.gob.ar/media/catalog/generos/data.json', 'generos'),
]


def download_resources_from_dataset(dataset):
    """Download the resources of a dataset.

    The resources will be downloaded in a folder named with the
    ids: <dataset_id>/<resource_id>. If the folder already exists,
    it will be assumed as already donwloaded and the process will
    continue with the next dataset.
    """
    try:
        os.mkdir(f"data/{dataset['identifier']}")
    except FileExistsError:
        pass

    resources = dataset['distribution']

    logging.info(f"Downloading {len(resources)} resources from dataset {dataset['title']}")

    for resource in resources:
        dir_name = f"data/{dataset['identifier']}/{resource['identifier']}"
        try:
            os.mkdir(dir_name)
        except FileExistsError:
            # If the resource directory already exists, asume it has been downloaded
            # and continue with the next resource
            continue
        url = resource.get('downloadURL')

        if url is None:
            logging.error(f"Resource {resource['title']} does not have a download URL")
            continue

        exit_value = os.system(
            f"wget --connect-timeout 3 -t 2 --no-check-certificate --directory-prefix '{dir_name}' -q {url}"
        )
        if exit_value != 0:
            logging.error(f"Error when downloading: {url}")
            continue


def download_data_portal(dcat_json):
    """Iterates through all the datasets of a DCAT file and download its resources"""
    datasets = dcat_json.get('dataset', None)
    if not datasets:
        logging.error("No datasets to download. Skipping.")
        return

    with multiprocessing.Pool(processes=16) as pool:
        pool.map(download_resources_from_dataset, datasets)

    logging.info(f"Finished downloading all resources from: {dcat_json.get('title', 'Title Not Found')}")


def get_dcat_json(url):
    """Gets the DCAT json."""
    try:
        response = requests.get(url, verify=url.startswith("https://"))
    except Exception as e:
        logging.error(f"Error getting data.json file: {e}")
        return dict()

    if response.status_code != 200:
        logging.info(f"Failed get the DCAT json from {url}. Status code: {response.status_code}")
        return dict()

    if "application/json" not in response.headers.get('Content-Type'):
        # Some portals migth get a redirect to Maintainance page, etc.
        logging.info(f"{url} did not contain a DCAT file {url}. Status code: {response.status_code}")
        return dict()

    return json.loads(response.content)


def zip_data_folder_and_dcat_file(dcat_json, portal_name):
    output_zip = f"{portal_name}.zip"

    # Dump the dcat_json into a file in data folder
    with open("./data/data.json", "w") as dcat_file:
        json.dump(dcat_json, dcat_file)

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('./data'):
            for file in files:
                full_path = os.path.join(root, file)
                # Add the file to the zip file, preserving the folder structure
                arcname = os.path.relpath(full_path, os.path.dirname("./data"))
                zipf.write(full_path, arcname)
    logging.info(f"Successfully created {output_zip} file.")


if __name__ == '__main__':
    """
    Get a local copy of all the DCAT files.
    If some of them fail, we'll get it manually and store it.
    Iterate through all of our DCAT files and download all the resources
    Write a zip file with the dcat file and all the data
    """
    for url, portal_name in _PORTALS:
        logging.info(f"Processing {url}...")
        try:
            shutil.rmtree('data')
        except FileNotFoundError:
            pass
        os.mkdir('data')
        dcat_json = get_dcat_json(url)
        if not dcat_json:
            logging.info(f"{url} did not retrieve a valid DCAT file. Continuing to next data portal...")
            continue
        download_data_portal(dcat_json)
        zip_data_folder_and_dcat_file(dcat_json, portal_name)
