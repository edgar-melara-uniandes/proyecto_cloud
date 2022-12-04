from cloud_storage_client import CloudStorageClient
import uuid
import os
import util

#variable entorno de docker //para usar este test debes agregar el archivo del service account es ela misma ruta que el test
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_.json_credential_file"

cloud_storage_client = CloudStorageClient()

def test_download_file():
    blob_name = "test-folder/test2.mp3"
    file_name = 'file-test'
    format_input = 'mp3'

    temp_path = str(uuid.uuid4())
    temporal_file_destination = util.create_temporal_file_destination(temp_path, file_name, format_input)

    
    cloud_storage_client.download_file(blob_name, temporal_file_destination)

    if os.path.exists(temporal_file_destination):
        print("Archivo descargado correctamene")
        util.delete_temporal_path(temp_path)

def test_upload_file():
    print("Subiendo archivo a cloud storage ......")
    cloud_storage_client.upload_file("test2.mp3","user_id/token_id/converted/test2.mp3")

def test_verify_if_file_exist():
    print("Verificando si archivo existe en cloud storage ......")
    cloud_storage_client.verify_if_file_exist("test2.mp3")

if __name__ == "__main__":
    test_download_file()
    test_upload_file()
    test_verify_if_file_exist()
    print("Running test in order to download blob from cloud storage")