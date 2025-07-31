#!/bin/bash
set -e

DB_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

run_up() {
  local version=$1
  local file=$(find /migrations -name "V${version}__*up.sql")
  echo "Applying $file"
  psql "$DB_URL" -f "$file"
}

run_down() {
  local version=$1
  local file=$(find /migrations -name "V${version}__*down.sql")
  echo "Reverting $file"
  psql "$DB_URL" -f "$file"
}

run_all_up() {
  for file in $(ls /migrations/V*__*up.sql | sort); do
    echo "Applying $file"
    psql "$DB_URL" -f "$file"
  done
}

run_all_down() {
  for file in $(ls /migrations/V*__*down.sql | sort -r); do
    echo "Reverting $file"
    psql "$DB_URL" -f "$file"
  done
}

run_test() {
  local versions=$(ls /migrations | grep "_up.sql" | sed -E 's/V([0-9]+)__.*_up\.sql/\1/' | sort -n | uniq)

  TMP_BEFORE="/tmp/schema_before.sql"
  TMP_AFTER="/tmp/schema_after.sql"

  for version in $versions; do
    local up_file=$(find /migrations -name "V${version}__*up.sql")
    local down_file=$(find /migrations -name "V${version}__*down.sql")

    echo "Testing V$version"

    psql "$DB_URL" -f "$up_file"
    pg_dump --schema-only "$DB_URL" > "$TMP_BEFORE"
    psql "$DB_URL" -f "$down_file"
    psql "$DB_URL" -f "$up_file"
    pg_dump --schema-only "$DB_URL" > "$TMP_AFTER"

    if diff "$TMP_BEFORE" "$TMP_AFTER" > /dev/null; then
      echo "V$version is idempotent"
    else
      echo "V$version is NOT idempotent"
      diff "$TMP_BEFORE" "$TMP_AFTER"
    fi

    echo "-------------------------"
  done
}

case "$1" in
  up)
    if [ "$2" = "all" ]; then
      run_all_up
    else
      run_up "$2"
    fi
    ;;
  down)
    if [ "$2" = "all" ]; then
      run_all_down
    else
      run_down "$2"
    fi
    ;;
  test)
    run_test
    ;;
  *)
    echo "No such command"
    ;;
esac
