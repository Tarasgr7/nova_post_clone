from pydantic import BaseModel

class BranchBase(BaseModel):
    name: str
    city: str
    address: str
    phone:str

class BranchCreate(BranchBase):
    pass

class BranchResponse(BranchBase):
    id: int

    class Config:
        from_attributes = True