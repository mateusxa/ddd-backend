from logging import error


class Error(Exception):

    message: str
    code: str
    status_code: int
    payload: dict | None

    def __init__(self, code: str, message: str, status_code: int = 500, payload: dict | None = None):            
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.payload = payload
        
        if status_code == 500:
            error(message)

    def to_dict(self):
        return {
            "code": self.code if self.code != 500 else "internalServerError",
            "message": self.message if self.code != 500 else "internal server error",
        }
    

    class Code:

        missing_attributes = "MissingAtributes"
        internal_error = "InternalError"


        invalid_json = "invalidJson"


        dict_incomplete = "dictIncomplete"
        duplicated_entities = "duplicatedEntities"
        object_not_found = "objectNotFound"
        duplicated_attribute = "duplicatedAttribute"
        invalid_attribute = "invalidAttribute"
        token_expired = "tokenExpired"

    
    class Message:

        missing_attributes = "Missing following attributes in json: {attributes}"

