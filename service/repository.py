from typing import Generic, Optional, Type, TypeVar
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import Base
from service.base import Repository


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """_summary_

    Args:
        Repository (_type_): _description_
        Generic (_type_): _description_
    """
    def __init__(self, model: Type[ModelType]) -> None:
        self._model = model
    
    
    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: CreateSchemaType,
        
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj=obj_in)
        db_obj = self._model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def get(self, db: AsyncSession, username: str | None =None) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.username == username)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()