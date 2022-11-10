#! /bin/bash

docker compose up --build --exit-code-from tests 2>/dev/null
