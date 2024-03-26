from firebase_admin import storage
from infrastructure.firebase import Firebase


class FirebaseStorage(Firebase):

    project_id = "xpa-engenharia"

    @staticmethod
    def upload_blob_by_path(source_filename, folder: str, filename: str) -> str:
        """Uploads a file to the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"
        # The path to your file to upload
        # source_filename = "local/path/to/file"
        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"

        destination_blob_name = f"{folder}/{filename}"

        bucket = storage.bucket()
        blob = bucket.blob(destination_blob_name)

        # Optional: set a generation-match precondition to avoid potential race conditions
        # and data corruptions. The request to upload is aborted if the object's
        # generation number does not match your precondition. For a destination
        # object that does not yet exist, set the if_generation_match precondition to 0.
        # If the destination object already exists in your bucket, set instead a
        # generation-match precondition using its generation number.
        generation_match_precondition = 0

        blob.upload_from_filename(source_filename, if_generation_match=generation_match_precondition)

        return f"gs://{FirebaseStorage.project_id}.appspot.com/{folder}/{filename}"


    @staticmethod
    def delete_blob(blob_name):
        """Deletes a blob from the bucket."""
        # bucket_name = "your-bucket-name"
        # blob_name = "your-object-name"    


        bucket = storage.bucket()
        blob = bucket.blob(blob_name)
        generation_match_precondition = None

        # Optional: set a generation-match precondition to avoid potential race conditions
        # and data corruptions. The request to delete is aborted if the object's
        # generation number does not match your precondition.
        blob.reload()  # Fetch blob metadata to use in generation_match_precondition.
        generation_match_precondition = blob.generation

        blob.delete(if_generation_match=generation_match_precondition)