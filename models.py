from pydantic import BaseModel, Field

class HeroModel(BaseModel):
    name: str
    real_name: str = Field(default="", serialization_alias="real name")
    universe: str
    
    model_config = {"populate_by_name": True}
