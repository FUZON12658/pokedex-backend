from db import Base
from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy import Text
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

"""
class Pokemon:
  id str
  name str
  image str
  type str
"""

class Pokemon(Base):
    __tablename__ = "pokemons"

    id =  Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50))
    type = Column(String(100))
    image_urls = Column(ARRAY(String), nullable=True)

    def __repr__(self) -> str:
        return f"<Pokemon(name={self.name}, type={self.type}, image_urls={self.image_urls})>"