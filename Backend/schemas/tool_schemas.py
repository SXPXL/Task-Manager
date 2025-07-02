"""
Tool Schemas
------------
Defines Pydantic schemas for tool creation and output/response.

Classes:
- ToolBase: Base schema for tool data
- ToolCreate: For creating a new tool
- ToolOut: For sending tool details in API responses
"""

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