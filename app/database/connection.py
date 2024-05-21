import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

url = "mongodb://127.0.0.1:27017/?directConnection=true"
client = AsyncIOMotorClient(url)


db = client.sampleDB
