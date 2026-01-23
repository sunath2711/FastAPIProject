from pydantic import BaseModel, ConfigDict, Field #Basemodel - is the basemodel from which all model are inherited ConfigDict to configure models, fields set constraints


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100) #title 
    content: str = Field(min_length=1)
    author: str = Field(min_length=1,max_length=50)


class PostCreate(PostBase):
    pass

class PostResponse(PostBase):  #these fields or this class is what we return from the API
    model_config = ConfigDict(from_attributes=True) # enable to read objects from attributes and not just dictionary #setup for data bases later

    id: int
    date_posted: str

