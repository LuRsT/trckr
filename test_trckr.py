import pytest

from trckr import app


class _FakeRedis:
    def __init__(self):
        self.data = {}

    async def set(self, key, value):
        self.data[key] = value

    async def get(self, key):
        return self.data.get(key)


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def fake_redis():
    redis = _FakeRedis()
    app.config["redis_client"] = redis
    yield redis
    del app.config["redis_client"]


@pytest.mark.asyncio
async def test_index(client):
    response = await client.get("/")

    assert response.status_code == 200
    assert await response.get_data(as_text=True) == "Nothing to see here."


@pytest.mark.asyncio
async def test_counter_missing_id(client):
    response = await client.get("/counter.txt")

    assert response.status_code == 200
    data = await response.get_data(as_text=True)
    assert "Counter not configured correctly" in data


@pytest.mark.asyncio
async def test_malformed_query_string(client):
    response = await client.get("/counter.txt?noid")

    assert response.status_code == 200
    data = await response.get_data(as_text=True)
    assert "Counter not configured correctly" in data


@pytest.mark.asyncio
async def test_query_string_with_wrong_key(client):
    response = await client.get("/counter.txt?noid=id")

    assert response.status_code == 200
    data = await response.get_data(as_text=True)
    assert "Counter not configured correctly" in data


@pytest.mark.asyncio
async def test_counter_records_view(client, fake_redis):
    response = await client.get("/counter.txt?id=myproject")

    assert response.status_code == 200
    assert await response.get_data(as_text=True) == "Every request counts"

    assert len(fake_redis.data) == 1
    key = list(fake_redis.data.keys())[0]
    assert key.startswith("myproject.")
