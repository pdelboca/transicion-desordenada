import json
import logging
import multiprocessing
import os
import sys

logging.basicConfig(filename="logs.txt", level=logging.INFO, format="")


def _get_folder_name():
    """Get the name of the folder where the data will be stored.

    It will be the name of the file without the `data.json`. For example,
    if the file is `energia.data.json`, the folder will be `energia`.
    """
    return sys.argv[1].split('.')[0]


def download_resources_from_dataset(dataset):
    """Download the resources of a dataset.

    The resources will be downloaded in a folder named with the ids: <dataset_id>/<resource_id>.
    """
    folder_name = _get_folder_name()
    try:
        os.mkdir(f"{folder_name}/{dataset['identifier']}")
    except FileExistsError:
        pass

    resources = dataset['distribution']

    logging.info(f"Downloading {len(resources)} resources from dataset {dataset['title']}")

    for resource in resources:
        dir_name = f"{folder_name}/{dataset['identifier']}/{resource['identifier']}"
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

        os.system(f"wget --no-check-certificate --directory-prefix '{dir_name}' -q {url}")


if __name__ == '__main__':
    file_path = sys.argv[1]

    data = {}
    with open(file_path, 'r') as f:
        data = json.load(f)
    datasets = data['dataset']

    # Create a folder with the name of the file to store the data
    try:
        os.mkdir(_get_folder_name())
    except FileExistsError:
        pass

    with multiprocessing.Pool(processes=16) as pool:
        pool.map(download_resources_from_dataset, datasets)

    logging.info("Finished downloading all resources")
