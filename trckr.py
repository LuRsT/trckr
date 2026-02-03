import datetime
import os

import redis.asyncio as aioredis
from quart import Quart, request

app = Quart(__name__)

PROJECT_KEY_TEMPLATE = "{project}.{date}"
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost")
HEADER_KEYS_TO_STORE = ["Remote-Addr", "Host", "User-Agent"]


def _get_redis():
    """Returns the Redis client. Can be overridden via app.config['redis_client']."""
    if "redis_client" in app.config:
        return app.config["redis_client"]
    return aioredis.from_url(REDIS_URL)


@app.route("/")
async def index():
    return "Nothing to see here."


@app.route("/counter.txt")
async def counter():
    project_id = request.args.get("id")
    if not project_id:
        return "Counter not configured correctly. URL is counter.txt?id=<PROJECTID>"

    date = str(datetime.datetime.now())

    await save_view(request.headers, project_id, date)
    return "Every request counts", {"Content-Type": "text/plain"}


async def save_view(request_headers, project_id, date):
    redis_connection = _get_redis()
    key = PROJECT_KEY_TEMPLATE.format(project=project_id, date=date)
    value = ",".join([request_headers.get(k) for k in HEADER_KEYS_TO_STORE])

    await redis_connection.set(key, value)
