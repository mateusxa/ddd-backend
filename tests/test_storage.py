import pytest
from random import randint
from infrastructure.storage.storage import Storage


def test_upload_blob():
    try:
        Storage.upload_file_to_folder(
            folder = f"folder_{randint(1, 99999)}",
            filename = "file",
            file_path = "tests/file.pdf",
        )
    except Exception:
        pytest.fail(str(Exception))


def test_delete_blob():
    number = randint(1, 99999)
    Storage.upload_file_to_folder(
        folder = f"folder_{number}",
        filename = "file",
        file_path = "tests/file.pdf",
    )

    try:
        Storage.delete_file_from_folder(
            folder = f"folder_{number}",
            filename = "file",
        )
    except Exception:
        pytest.fail(str(Exception))



