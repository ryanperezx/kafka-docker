FROM library/postgres:13.15-bookworm
RUN apt-get update && apt-get install -y postgresql-13-wal2json
COPY init.sql /docker-entrypoint-initdb.d/