

class DefaultError(Exception):
    pass


class DictIncomplete(DefaultError):
    pass


class ObjectNotFound(DefaultError):
    pass


class DuplicatedAttribute(DefaultError):
    pass


class DuplicatedEntities(DefaultError):
    pass


class InvalidAttribute(DefaultError):
    pass


class TokenExpired(DefaultError):
    pass
