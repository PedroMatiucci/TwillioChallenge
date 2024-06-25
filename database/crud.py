from google.cloud import storage

class Crud:


    def __init__(self):
        self.bucket_name = "twillio-script-bucket"
        self.credentials_file = "credentials.json"

    def upload_to_gcs(self, source_file_path, destination_blob_name):
        storage_client = storage.Client.from_service_account_json(self.credentials_file)
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_path, content_type='audio/ogg')
        return blob.public_url
