from pydantic import BaseModel

class ToolBase(BaseModel):
    """
    Schema for storing tool details.

    Attributes:
    name (str): Stores the name of the tool.
    """
    name: str

class ToolCreate(ToolBase):
    pass

class ToolOut(ToolBase):
    """
    Schema for sending tool details in responses.

    Attributes:
    id (int): For sending the ID of the tool.
    """
    id: int

    class Config:
        orm_mode = True