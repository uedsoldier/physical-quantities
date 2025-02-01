@echo off
setlocal

set DB_NAME=mock_database.db
set SQL_SCRIPT=create_mock_database.sql

if not exist %DB_NAME% (
    echo Creating mock database...
    echo .exit | sqlite3 %DB_NAME%
)

sqlite3 %DB_NAME% < %SQL_SCRIPT%

echo SQLite database created
