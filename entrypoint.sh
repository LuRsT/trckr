#!/bin/sh

uv run hypercorn --log-level debug -b 0.0.0.0:$PORT trckr:app
