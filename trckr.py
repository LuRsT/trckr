import datetime
import os

import aioredis
from quart import Quart, request

app = Quart(__name__)

PROJECT_KEY_TEMPLATE = "{project}.{date}"
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost")
HEADER_KEYS_TO_STORE = ["Remote-Addr", "Host", "User-Agent"]


@app.route("/")
async def index():
    return "Nothing to see here."


@app.route("/counter.txt")
async def counter():
    await request.get_data()
    try:
        project_id = request.query_string.decode().split("=")[1]
    except Exception:
        return "Counter not configured correctly. URL is counter.js?id=<PROJECTID>"

    date = str(datetime.datetime.now())

    await save_view(request.headers, project_id, date)
    return "Every request counts", {"Content-Type": "text/plain"}


async def save_view(request_headers, project_id, date):
    redis_connection = await aioredis.create_redis(REDIS_URL)
    key = PROJECT_KEY_TEMPLATE.format(project=project_id, date=date)
    value = ",".join([request_headers.get(key) for key in HEADER_KEYS_TO_STORE])

    await redis_connection.set(key, value)
