from datetime import datetime, timezone
from random import randint
import uuid
from infrastructure.firebase.firestore import Firestore


firestore = Firestore()
collection = "firestore"

def test_create_and_get_document():
    id = str(uuid.uuid4())
    data = {
        "name": f"testting{randint(1111, 9999)}",
        "created": datetime.now(timezone.utc)
    }

    created_data = firestore.create_document(collection=collection, id=id, data=data)

    got_data = firestore.get_document_by_id(collection=collection, id=id)

    assert got_data
    assert id == got_data["id"]
    assert created_data["name"] == got_data["name"]
    assert created_data["created"] == got_data["created"]


def test_update_document():
    id = str(uuid.uuid4())
    data = {
        "name": f"testting{randint(1111, 9999)}",
        "created": datetime.now(timezone.utc)
    }

    created_data = firestore.create_document(collection=collection, id=id, data=data)

    update_data = {
        "name": f"updated_testting{randint(1111, 9999)}",
    }
    got_data = firestore.update_document(collection=collection, id=id, data=update_data)

    assert got_data
    assert id == got_data["id"]
    assert update_data["name"] == got_data["name"]
    assert created_data["created"] == got_data["created"]


def test_get_documents_by_criteria():
    id = str(uuid.uuid4())
    name = f"testting{randint(1111, 9999)}"
    data = {
        "name": name,
        "created": datetime.now(timezone.utc)
    }

    firestore.create_document(collection=collection, id=id, data=data)

    document_list = firestore.get_documents_by_criteria(
        collection=collection,
        limit=1,
        name=name
    )
    assert len(document_list) == 1
    assert document_list[0]["name"] == name


# def test_page_documents_by_criteria():
#     name = f"testting{randint(1111, 9999)}"
#     data = {
#         "name": name,
#         "created": datetime.now(timezone.utc)
#     }

#     for _ in range(6):
#         id = str(uuid.uuid4())
#         firestore.create_document(collection=collection, id=id, data=data)

#     cursor = None
#     while True:
#         old_cursor = cursor
#         cursor, document_list = firestore.page_documents_by_criteria(
#             collection=collection,
#             start_after=cursor,
#             limit=2,
#             name=name
#         )

#         print(f"cursor - {cursor}")
#         print(f"document_list - {document_list}")

#         if old_cursor:
#             assert old_cursor != cursor
#         assert len(document_list) == 2
#         for document in document_list:
#             assert document["name"] == name

#         if not cursor:
#             break


def test_delete_document():
    id = str(uuid.uuid4())
    data = {
        "name": f"testting{randint(1111, 9999)}",
        "created": datetime.now(timezone.utc)
    }

    firestore.create_document(collection=collection, id=id, data=data)

    firestore.delete_document(collection=collection, id=id)


