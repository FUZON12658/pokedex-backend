from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import uuid

class PokemonModel(BaseModel):
  id:uuid.UUID
  name:str
  type:str
  image_urls:Optional[List[str]] = []

  model_config = ConfigDict(
    from_attributes=True
  )
