# TODO remove
import uuid


data = []


class Repository:

    @staticmethod
    def get_by_id(id: str) -> dict | None:
        for d in data:
            if d.get("id") == id:
                return d
        return None

    @staticmethod
    def get_all():
        return data

    @staticmethod
    def save(dict: dict):
        dict["id"] = str(uuid.uuid4())
        dict["bucket_url"] = str(uuid.uuid4())
        data.append(dict)
        return dict

    @staticmethod
    def delete(id: str) -> None:
        for d in data:
            if d.get("id") == id:
                data.remove(d)
                return
        raise ValueError(f"No dictionary with id {id} found")