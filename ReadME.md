# North Sussex Judo Management Application

This document provides instructions for setting up and running the North Sussex Judo Management application. It supports both Microsoft SQL Server and SQLite3 databases.

## Table of Contents

1.  [Prerequisites](#prerequisites)
2.  [Setup for MS SQL Server](#setup-for-ms-sql-server)
    *   [Install MS SQL Server](#install-ms-sql-server)
    *   [Install pyodbc and ODBC Driver](#install-pyodbc-and-odbc-driver)
    *   [Configure Database Connection](#configure-database-connection)
    *   [Create the Database](#create-the-database)
3.  [Setup for SQLite3](#setup-for-sqlite3)
    *   [Install SQLite3](#install-sqlite3)
4.  [Running the Application](#running-the-application)
5.  [Troubleshooting](#troubleshooting)

## 1. Prerequisites

*   **Python 3.6 or higher**
*   **pip** (Python package installer)

## 2. Setup for MS SQL Server

This section outlines the steps to set up the application to use a Microsoft SQL Server database.

### 2.1 Install MS SQL Server

If you don't have it already, you need to install MS SQL Server. There are multiple editions available, including a free Developer Edition.

1.  Download MS SQL Server from the official Microsoft website: [https://www.microsoft.com/sql-server/sql-server-downloads](https://www.microsoft.com/sql-server/sql-server-downloads)
2.  Follow the installation instructions.
3.  Make sure you have the server name, database name, username, and password for later steps.

### 2.2 Install `pyodbc` and ODBC Driver

1.  **Install `pyodbc`:**
    Open a terminal or command prompt and run:

    ```bash
    pip install pyodbc
    ```
2.  **Install Microsoft ODBC Driver for SQL Server:**
    *   Download the appropriate ODBC Driver from Microsoft:  [https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
    *   Install the downloaded driver. Make a note of the exact driver name; you'll need it in the next step.

### 2.3 Configure Database Connection

1.  Open the `database.py` file.
2.  Locate the following lines:

    ```python
    SERVER = 'your_server_name'  # Replace with your server name
    DATABASE = 'your_database_name' # Replace with your database name
    USERNAME = 'your_username' # Replace with your username
    PASSWORD = 'your_password'  # Replace with your password
    DRIVER = '{ODBC Driver 17 for SQL Server}' # Or your appropriate driver
    ```
3.  **Replace the placeholders** with your actual SQL Server connection details and the correct driver name.
    *   `SERVER`: The name or IP address of your SQL Server instance.
    *   `DATABASE`: The name of the database you want to use for this application.
    *   `USERNAME`: The username to connect to the SQL server
    *   `PASSWORD`: The password for the username
    *   `DRIVER`: The exact name of the ODBC driver you installed (e.g., `{ODBC Driver 17 for SQL Server}`). This **must** match exactly, including curly braces.

### 2.4 Create the Database

1.  **Connect to your SQL Server** using SQL Server Management Studio (SSMS) or another SQL client.
2.  **Create the database** if it does not already exist using the value you provided for the DATABASE constant.
3.  **Run the schema script:** Navigate to the `north_sussex_judo_schema.sql` file in the explorer and run it. This will create the required tables.  **Important:** The provided `north_sussex_judo_schema.sql` may need adjustments for compatibility with MS SQL Server syntax. You will likely need to:
    * Change data types to match SQL Server (e.g., use `INT` rather than `INTEGER`, use `DATETIME` instead of `TEXT`, etc.)
    * Change `AUTOINCREMENT` to `IDENTITY (1,1)`
    * other adjustments as required

## 3. Setup for SQLite3

This section describes how to set up the application with an SQLite3 database.

### 3.1 Install SQLite3

SQLite3 is usually included by default in Python. If it is not available install with `pip install sqlite3`.
No further action is required if you just want to run using SQLite.

## 4. Running the Application

1.  **Ensure that you have configured the database connection correctly** in `database.py` as explained in step 2 or have decided to use SQLite.
2.  **Navigate to the project directory** in your terminal or command prompt.
3.  **Run the application** using the following command:
    ```bash
    python main.py
    ```
4.  The login window will open, if there are no users in the database you can create one.
5.  Log in and start using the application to manage athletes, training plans, competitions, and generate reports.

## 5. Troubleshooting

*   **Database Connection Errors:** Double-check the database connection details in `database.py`, and ensure the database server is running.
*   **ODBC Driver Issues:** Verify that the ODBC driver is installed correctly and that the driver name in `database.py` matches exactly.
*   **SQL Syntax Errors:**  If you see errors related to SQL syntax, make sure your SQL queries are compatible with the database you're using (MS SQL Server or SQLite3).
*   **Table Does Not Exist:** Ensure that the schema has been run on the correct database.
*   **General Errors:** Always check the output and traceback for any other specific errors.

 <a href="https://huggingface.co/Golgrax/GyroUIapk/resolve/main/sample%20video.mkv" style="display: inline-block; padding: 10px 20px; font-size: 16px; text-align: center; text-decoration: none; background-color: #4CAF50; color: white; border-radius: 5px;">Download Sample Video</a>