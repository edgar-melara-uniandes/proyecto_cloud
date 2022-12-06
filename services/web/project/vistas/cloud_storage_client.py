# Imports the Google Cloud client library
from google.cloud import storage
import os

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./path_to_your_.json_credential_file"

#Para desarrollo local reemplazar el nombre del BUCKET_NAME
BUCKET_NAME = os.environ.get("BUCKET_NAME", "music-converter-prueba-1")

class CloudStorageClient:

    # Instantiates a client
    storage_client = storage.Client()

    def download_file(self, source_blob_name, destination_file_name):
        self.__download_blob(BUCKET_NAME, source_blob_name, destination_file_name)

    def upload_file(self, source_file_name, destination_blob_name):
        self.__upload_blob(BUCKET_NAME, source_file_name, destination_blob_name)
        return 'temporal_file_path'

    def verify_if_file_exist(self, blob_name):
        return self.__verify_blob(BUCKET_NAME, blob_name)
    
    def delete_folder(self, folder_name):
        self.__delete_folder(BUCKET_NAME, folder_name)
        
    def delete_blob(self, blob_name):
        self.__delete_blob(BUCKET_NAME, blob_name)

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

    def __verify_blob(self, bucket_name, blob_name):
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.get_blob(blob_name)
        if not blob is None:
            print(f'Blob encontrado: {blob}')
            return True
        else:
            print(f'Blob: {blob_name}, no existe en cloud storage')
            return False
        

    def __upload_blob(self, bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"
        # The path to your file to upload
        # source_file_name = "local/path/to/file"
        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"

        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        print(
            f"File {source_file_name} uploaded to {destination_blob_name}."
        )
    
    def __delete_folder(self, bucket_name, folder_name):
        bucket = self.storage_client.get_bucket(bucket_name)
        """Delete object under folder"""
        blobs = list(bucket.list_blobs(prefix=folder_name))
        bucket.delete_blobs(blobs)
        print(f"Folder {folder_name} deleted.")
    
    def __delete_blob(self, bucket_name, blob_name):
        """Deletes a blob from the bucket."""
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()
        print(f"Blob {blob_name} deleted.")