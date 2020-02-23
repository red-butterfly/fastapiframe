from pydantic import BaseModel


class ResponseItem(BaseModel):
    msg: str


class TestInItem(BaseModel):
    name: str
    description: str = None
    language: str = 'python'
    type: str = 'web'


class TestOutItem(BaseModel):
    id: int
    name: str
    description: str = None
    language: str = None
    type: str = None