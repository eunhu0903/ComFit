from pydantic import BaseModel

class CommitCreate(BaseModel):
    type: str
    duration: int
    sets: int
    intensity: str
    memo: str

class CommitResponse(BaseModel):
    id: int
    type: str
    duration: int
    sets: int
    intensity: str
    memo: str

    class Config:
        from_attributes = True