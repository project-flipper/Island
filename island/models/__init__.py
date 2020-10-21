from pydantic import BaseModel

class ORM_Model(BaseModel):
    class Config:
        orm_mode = True