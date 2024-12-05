from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://pavel:popov@mongo:27017/iotdata?authSource=admin"
client = AsyncIOMotorClient(MONGO_URI)
db = client.iotdata
data = db.data
instant = db.instant
ongoing = db.ongoing