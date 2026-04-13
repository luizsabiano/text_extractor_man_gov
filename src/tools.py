import os
import json

from os import getcwd
JSON_PATH = getcwd() + "/data/chunks/"


def load_name_list_json(JSON_PATH):
    collection_list = []
    directory = os.listdir(JSON_PATH)
    if len(directory) != 0:
        arquivos = os.listdir(JSON_PATH)

        for arquivo in arquivos:
            if not arquivo.startswith('.'):
                collection_list.append(JSON_PATH + arquivo)

        del arquivos

        return collection_list
    return None


def files_json_to_dict(path):
    if os.path.exists(path):
        # Load json file and convert to dict
        with open(file=path, mode='r') as arquivo:
            dict_list = json.load(arquivo)
            return dict_list
    else:
        return None




