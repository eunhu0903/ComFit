from pydantic import BaseModel

class UserProfileResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True
