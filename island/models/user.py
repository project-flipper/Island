from island.models import ORM_Model

class UserBase(ORM_Model):
    id: int
    username: str
    nickname: str

class UserDB(UserBase):
    password: str 
