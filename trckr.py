import datetime
import asyncio
import aioredis
import redis
from quart import Quart, request

app = Quart(__name__)
sr = redis.StrictRedis(host="localhost", port=6379)

PROJECT_KEY_TEMPLATE = "{project}.{date}"
REDIS_URL = "redis://localhost"
HEADER_KEYS_TO_STORE = ["Remote-Addr", "Host", "User-Agent"]


@app.route("/")
async def index():
    return "Nothing to see here."


@app.route("/counter.js")
async def counter():
    await request.get_data()
    project_id = request.query_string.decode().split("=")[1]
    date = str(datetime.datetime.now())

    await save_view(request.headers, project_id, date)
    return ""


async def save_view(request_headers, project_id, date):
    key = PROJECT_KEY_TEMPLATE.format(project=project_id, date=date)
    value = ",".join([request_headers.get(key) for key in HEADER_KEYS_TO_STORE])

    redis_connection = await aioredis.create_redis(REDIS_URL)
    await redis_connection.set(key, value)


if __name__ == "__main__":
    app.run("localhost", port=5000, debug=True)