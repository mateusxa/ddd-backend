from datetime import datetime, timezone
from random import randint
import uuid
from infrastructure.firebase.firestore import Firestore


firestore = Firestore()
collection = "firestore"


def test_create_and_get_document():
    data = {
        "name": f"testting{randint(1111, 9999)}",
        "created": datetime.now(timezone.utc)
    }

    created_data = firestore.create(collection=collection, data=data)
    assert created_data

    got_data = firestore.get_by_id(collection=collection, id=created_data["id"])

    assert got_data
    assert created_data["id"] == got_data["id"]
    assert created_data["name"] == got_data["name"]
    assert created_data["created"] == got_data["created"]


def test_update():
    data = {
        "name": f"testting{randint(1111, 9999)}",
        "created": datetime.now(timezone.utc)
    }

    created_data = firestore.create(collection=collection, data=data)
    assert created_data

    update_data = {
        "id": created_data["id"],
        "name": f"updated_testting{randint(1111, 9999)}",
    }
    got_data = firestore.update(collection=collection, data=update_data)

    assert got_data
    assert created_data["id"] == got_data["id"]
    assert update_data["name"] == got_data["name"]
    assert created_data["created"] == got_data["created"]


def test_get_all_by_criteria():
    
    name = f"testting{randint(1111, 9999)}"
    data = {
        "id": str(uuid.uuid4()),
        "name": name,
        "created": datetime.now(timezone.utc)
    }

    firestore.create(collection=collection, data=data)

    document_list = firestore.get_by_fields(
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
#         firestore.create(collection=collection, id=id, data=data)

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

def test_page():
    name = f"testting{randint(1111, 9999)}"

    for _ in range(6):
        firestore.create(collection=collection, data={
        "name": name,
        "created": datetime.now(timezone.utc)
    })

    cursor = None
    while True:
        old_cursor = cursor
        cursor, document_list = firestore.page(
            collection=collection,
            cursor=cursor,
            limit=2,
            name=name,
        )
        if not cursor:
            break

        if old_cursor:
            assert old_cursor != cursor
        assert len(document_list) == 2
        for document in document_list:
            if document:
                assert document["name"] == name


def test_delete():
    id = str(uuid.uuid4())
    data = {
        "id": id,
        "name": f"testting{randint(1111, 9999)}",
        "created": datetime.now(timezone.utc)
    }

    firestore.create(collection=collection, data=data)

    firestore.delete(collection=collection, id=id)


