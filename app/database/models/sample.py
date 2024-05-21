from datetime import datetime
from pydantic import Field

from .base import Base, ObjectId
from app.database.connection import db


class Sample(Base):
    id: ObjectId = Field(alias="_id")
    value: int
    timestamp: datetime = Field(alias="dt")

    @classmethod
    async def filter_by_date_range(cls, start_date: datetime, end_date: datetime):
        filter = {
            'dt': {
                "$gte": start_date,
                "$lte": end_date
            }
        }
        return  await cls.filter(filter)

Sample.set_collection('sample_collection')
