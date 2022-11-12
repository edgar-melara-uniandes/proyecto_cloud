# Imports the Google Cloud client library
from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_.json_credential_file"
os.environ["BUCKET_NAME"] = "music-converter-prueba-1"

BUCKET_NAME = os.environ.get("BUCKET_NAME", "music-converter-prueba-1")

class CloudStorageClient:

    # Instantiates a client
    storage_client = storage.Client()

    def get_binary_file_from_cloud_storage(self, source_blob_name, destination_file_name):

        self.__download_blob(BUCKET_NAME, source_blob_name, destination_file_name)

    def save_file_in_disk(self, binary_file):
        return 'temporal_file_path'

    def push_file(self, file_path, file):
        return True

    def __download_blob(self, bucket_name, source_blob_name, destination_file_name):
        """Downloads a blob from the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        # The ID of your GCS object
        # source_blob_name = "storage-object-name"

        # The path to which the file should be downloaded
        # destination_file_name = "local/path/to/file"

        bucket = self.storage_client.bucket(bucket_name)

        # Construct a client side representation of a blob.
        # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
        # any content from Google Cloud Storage. As we don't need additional data,
        # using `Bucket.blob` is preferred here.
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

        print(
            "Downloaded storage object {} from bucket {} to local file {}.".format(
                source_blob_name, bucket_name, destination_file_name
            )
        )