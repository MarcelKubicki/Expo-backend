from redis import asyncio as aioredis
from src.config import Config

TOKEN_EXPIRY = 3600

token_blocklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0
)


async def add_jti_to_blocklist(jti: str):
    await token_blocklist.set(
        name=jti,
        value="",
        ex=TOKEN_EXPIRY
    )


async def is_token_in_blocklist(jti: str) -> bool:
    result = await token_blocklist.get(jti)
    return result is not None
