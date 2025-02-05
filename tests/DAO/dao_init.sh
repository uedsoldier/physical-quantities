#!/bin/bash

DB_NAME="mock_database.db"
SQL_SCRIPT="create_mock_database.sql"

if [ -f "$DB_NAME" ]; then
    echo "Deleting existing mock database..."
    rm "$DB_NAME"
fi

echo "Creating mock database..."
sqlite3 "$DB_NAME" ".exit"

if [ ! -f "$SQL_SCRIPT" ]; then
    echo "Error: $SQL_SCRIPT script not found."
    exit 1
fi

sqlite3 "$DB_NAME" < "$SQL_SCRIPT"

echo "SQLite database created"
