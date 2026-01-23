from pydantic import BaseModel, ConfigDict, Field #Basemodel - is the basemodel from which all model are inherited ConfigDict to configure models, fields set constraints


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)
    author: str = Field(min_length=1,max_length=50)


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_posted: str

