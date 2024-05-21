
import json
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.schemas.sample import SampleAggregateRequest
from app.services.sample import SampleService

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    print('Hello')
    first_name = message.from_user.full_name if message.from_user else ''
    await message.answer(f'Привет {first_name}')

@router.message(F.text)
async def json_handler(message: Message):
    text = message.text if message.text else ''
    request = SampleAggregateRequest(**json.loads(text))
    
    aggregate_dict = await SampleService.aggregate_by_period(request)
    
    response_json = json.dumps(aggregate_dict)

    await message.answer(response_json)
    