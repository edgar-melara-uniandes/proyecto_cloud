import os
from shutil import rmtree

def create_temporal_file_destination(temp_path, file_name, format_input):
    if not os.path.exists(temp_path):
        print(f"Creando carpeta temporal.......")
        os.makedirs(temp_path)
        print(f"carpeta temporal creada: {temp_path}")

    temporal_file_destination = f'{temp_path}/{file_name}.{format_input}'
    fp = open(temporal_file_destination, 'x')
    fp.close()
    return temporal_file_destination

def delete_temporal_path(temp_path):
    print(f"Eliminando carpeta temporal: {temp_path} .......")
    rmtree(temp_path)
    if not os.path.exists(temp_path):
        print("Carpeta temporal eliminado correctamene")