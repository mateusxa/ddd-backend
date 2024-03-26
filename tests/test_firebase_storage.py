from random import randint
import pytest
from infrastructure.firebase.storage import FirebaseStorage


def test_upload_blob():
    try:
        FirebaseStorage.upload_blob_by_path(
            folder = f"folder_{randint(1, 99999)}",
            filename= "file",
            source_filename = "tests/file.pdf",
        )
    except Exception:
        pytest.fail(str(Exception))


def test_delete_blob():
    number = randint(1, 99999)
    FirebaseStorage.upload_blob_by_path(
        folder = f"folder_{number}",
        filename= "file",
        source_filename = "tests/file.pdf",
    )

    try:
        FirebaseStorage.delete_blob(f"folder_{number}/file")
    except Exception:
        pytest.fail(str(Exception))



