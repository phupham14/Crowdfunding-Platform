#!/bin/sh
set -e

host="${DB_HOST:-localhost}"
port="${DB_PORT:-5432}"
user="${DB_USER:-postgres}"
database="${DB_NAME:-postgres}"

until PGPASSWORD="$DB_PASSWORD" psql -h "$host" -p "$port" -U "$user" -d "$database" -c '\q'; do
  echo "Postgres is unavailable at $host:$port - sleeping"
  sleep 2
done

echo "Postgres is up - executing command"
exec "$@"
