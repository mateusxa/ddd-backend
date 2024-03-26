from infrastructure.firebase.storage import FirebaseStorage


class Storage:

    @staticmethod
    def upload_file_to_folder(folder: str, filename: str, file_path: str) -> str:
        return FirebaseStorage.upload_blob_by_path(
            source_filename = file_path,
            folder = folder,
            filename = filename, 
        )
        
    
    @staticmethod
    def delete_file_from_folder(folder: str, filename: str):
        FirebaseStorage.delete_blob(f"{folder}/{filename}")