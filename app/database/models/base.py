from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorCursor
from bson.objectid import ObjectId as BsonObjectId
from pydantic import BaseModel

from app.database.connection import db


class ObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, d):

        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)

class Base(BaseModel):
    _collection: AsyncIOMotorCollection

    @classmethod
    async def get(cls, filter: dict):
        obj = await cls._collection.find_one(filter)
        return cls(**obj) if obj else None

    @classmethod
    async def filter(cls, filter):
        objs = cls._collection.find(filter)
        return await cls._to_list(objs)
    
    @classmethod
    async def _to_list(cls, objs: AsyncIOMotorCursor):
        return [cls(**u) async for u in objs]

    @classmethod
    def set_collection(cls, collection: str):
        cls._collection = db[collection]

    @classmethod
    def get_collection(cls):
        return cls._collection


    