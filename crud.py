from models import Pokemon
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select

class CRUD:
  async def get_pokemons(self, async_session: async_sessionmaker[AsyncSession]):
    async with async_session() as session:
      statement = select(Pokemon).order_by(Pokemon.id)
      result = await session.execute(statement)
      return result.scalars().all()