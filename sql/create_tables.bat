@echo off
chcp 65001 >nul
echo ========================================
echo SQL Server Table Creation Script
echo ========================================
echo.
echo This script will create the inspection_records table in SQL Server
echo Database: CPIC_QMI
echo Server: zjzx.cpicfiber.com
echo.
echo Please ensure you have:
echo 1. SQL Server Management Studio (SSMS) installed
echo 2. Access to the SQL Server database
echo 3. Appropriate permissions to create tables
echo.
echo ========================================
echo Instructions:
echo ========================================
echo.
echo 1. Open SQL Server Management Studio (SSMS)
echo 2. Connect to server: zjzx.cpicfiber.com
echo 3. Open the file: create_tables.sql
echo 4. Execute the script (Press F5 or click Execute)
echo 5. Verify the table was created successfully
echo.
echo ========================================
echo.
echo Opening create_tables.sql...
echo.

if exist "create_tables.sql" (
    start notepad "create_tables.sql"
    echo File opened successfully.
) else (
    echo ERROR: create_tables.sql not found!
    echo Please make sure you are running this script from the correct directory.
)

echo.
echo Press any key to exit...
pause >nul
