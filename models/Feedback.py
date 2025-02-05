from pydantic import BaseModel

class FeedBack(BaseModel):
    name: str
    message: str