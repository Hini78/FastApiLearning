from pydantic import BaseModel

class AgedUser(BaseModel):
    name: str
    age: int