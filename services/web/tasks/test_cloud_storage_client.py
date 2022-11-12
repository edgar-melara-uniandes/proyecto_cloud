from cloud_storage_client import CloudStorageClient
import uuid
import os

#variable entorno de docker
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_.json_credential_file"

BASE_TEMPORAL_FOLDER_FOR_FILES = os.environ.get("TEMPORAL_FOLDER_FOR_FILES", "tmp/music-converter/download/")
TEMPORAL_FOLDER = BASE_TEMPORAL_FOLDER_FOR_FILES

def test_download_file():

    blob_name = "test-folder/test2.mp3"
    uuid_string = str(uuid.uuid4())
    temp_path = TEMPORAL_FOLDER + uuid_string
    temporal_file_path = temp_path + "/" + "file_to_convert.mp3"

    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    fp = open(temporal_file_path, 'x')
    fp.close()

    cloud_storage_client = CloudStorageClient()
    cloud_storage_client.get_binary_file_from_cloud_storage(blob_name, temporal_file_path)

if __name__ == "__main__":
    test_download_file()
    print("Running test in order to download blob from cloud storage")