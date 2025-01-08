from pydantic import BaseModel

class UserProfileUpdate(BaseModel):
    username: str

class UserProfileResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
