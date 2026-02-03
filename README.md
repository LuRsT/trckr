# trckr

A minimalist traffic analyser

## How to build:

$ docker compose build

## How to start:

$ docker compose up

## How to use:

Requests to base_url/counter.txt?id=<yourid> will be stored in redis.

If you want to track the visits to a page, add a `<img src="BASE_URL/counter.txt?id=YOURID" />`
somewhere in the page, and visits will be tracked automatically.

Example:

```sh
$ curl http://localhost:8000/counter.txt?id=1
```
