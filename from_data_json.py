import json
import multiprocessing
import os
import sys

def download_dataset(dataset):
    folder_name = sys.argv[1].split('.')[0]
    try:
        os.mkdir(f"{folder_name}/{dataset['identifier']}")
    except FileExistsError:
        pass

    resources = dataset['distribution']

    for resource in resources:
        dir_name = f"{folder_name}/{dataset['identifier']}/{resource['identifier']}"
        try:
            os.mkdir(dir_name)
        except FileExistsError:
            # If the resource directory already exists, asume it has been downloaded
            # and continue with the next resource
            continue
        url = resource['downloadURL']
        print(f"Downloading {resource['title']}")
        os.system(f"wget --no-check-certificate --directory-prefix '{dir_name}' -q {url}")


if __name__ == '__main__':
    file_path = sys.argv[1]

    data = {}
    with open(file_path, 'r') as f:
        data = json.load(f)
    datasets = data['dataset']

    # Create a folder with the name of the file to store the data
    try:
        os.mkdir(file_path.split('.')[0])
    except FileExistsError:
        pass

    with multiprocessing.Pool(processes=4) as pool:
        pool.map(download_dataset, datasets)
