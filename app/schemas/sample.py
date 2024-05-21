from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime

class SampleAggregateTypeEnum(Enum):
    MONTH='month'
    DAY='day'
    HOUR='hour'

class SampleAggregateRequest(BaseModel):
    start_date: datetime = Field(alias='dt_from')
    end_date: datetime = Field(alias='dt_upto')
    type: SampleAggregateTypeEnum = Field(alias='group_type')