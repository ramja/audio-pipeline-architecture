#!/usr/bin/env bash
set -e
PORT=${PORT:-8082}
psql -f create_tables.sql

luigid --port "$PORT"
