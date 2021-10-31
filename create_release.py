#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import zipfile
import json
from config import ALI_AVD_DB_DB_PATH, ALI_AVD_DB_VERSION_FILE, DB_FILE_PREFIX_NAME


def read_db():
    db_path = os.path.join(os.getcwd(), ALI_AVD_DB_DB_PATH)
    for parent_path, _, file_names in os.walk(db_path):
        for file_name in file_names:
            file_path = os.path.join(parent_path, file_name)
            with open(file_path, 'r') as f:
                data = json.loads(f.read())
            for item in data:
                yield json.dumps(item)


def run():
    version_file_path = os.path.join(os.getcwd(), ALI_AVD_DB_VERSION_FILE)
    with open(version_file_path, 'r') as f:
        version = f.read().replace('-', '_')

    db_file_name = f'{DB_FILE_PREFIX_NAME}_{version}.json'
    db_path = os.path.join(os.getcwd(), db_file_name)
    with open(db_path, 'w') as f:
        f.write('[')
        is_first_write = True
        for data in read_db():
            if not is_first_write:
                f.write(', ')
            else:
                is_first_write = False
            f.write(data)
        f.write(']')

    db_zip_file_path = os.path.join(os.getcwd(), f'{DB_FILE_PREFIX_NAME}_{version}.zip')
    with zipfile.ZipFile(db_zip_file_path, 'w', zipfile.ZIP_DEFLATED) as f:
        f.write(db_file_name)

    print(f'{DB_FILE_PREFIX_NAME}_{version}.zip')


if __name__ == '__main__':
    run()
