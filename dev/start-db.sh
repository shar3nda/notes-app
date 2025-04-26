#!/usr/bin/env bash
export ROOT_DIR="$(realpath $(dirname $(dirname "$0")))"
source "$ROOT_DIR/src/.env.dev"

docker run --name notes-app-db \
  -e "POSTGRES_USER=$POSTGRES_USER" \
  -e "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" \
  -e "POSTGRES_DB=$POSTGRES_DB" \
  -p 5432:5432 \
  -v notes-app_pgdata:/var/lib/postgresql/data \
  -d postgres:17.4-bookworm
