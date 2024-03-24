import uuid


def generate_id() -> str:
    return str(uuid.uuid4())


def get_class_name(obj: object):
    return get_plural_name(obj.__class__.__name__.lower())


def get_class_name_by_id(obj: object):
    return get_plural_name(obj.__class__.__name__.lower()[:-2])


def get_plural_name(name: str):
    return name + "s" if name[-1] != "y" else name[:-1] + "ies"
