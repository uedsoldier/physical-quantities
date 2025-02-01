#!/bin/bash

DB_NAME="mock_database.db"
SQL_SCRIPT="create_mock_database.sql"

if [ ! -f "$DB_NAME" ]; then
    echo "Creating mock database..."
    sqlite3 "$DB_NAME" ".exit"
fi

sqlite3 "$DB_NAME" < "$SQL_SCRIPT"

echo "SQLite database created"
