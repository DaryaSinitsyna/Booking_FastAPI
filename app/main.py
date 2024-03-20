from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.config import settings
from app.hotels.models import Hotels  # noqa
from app.users.models import Users  # noqa
from app.hotels.rooms.models import Rooms  # noqa
from app.bookings.models import Bookings  # noqa

from app.bookings.router import router as router_bookings
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
from app.users.router import router_auth, router_users

from app.pages.router import router as router_pages
from app.images.router import router as router_images

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis


@asynccontextmanager
async def lifespan(app: FastAPI):
    # выполняется при запуске
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
                              encoding="utf8",
                              decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(
    title='Booking hotels',
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_bookings)
app.include_router(router_rooms)

app.include_router(router_pages)
app.include_router(router_images)

origins = [
    'http://localhost:8000', '192.168.0.101', 'http://192.168.0.104:8000', 'http://localhost',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers", "Authorization",
                   "Access-Control-Allow-Credentials"],
    expose_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers",
                    "Access-Authorization", "Access-Control-Allow-Credentials", "Authorization"]
)
