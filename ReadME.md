# North Sussex Judo Management Application

This document provides instructions for setting up and running the North Sussex Judo Management application. The application uses **Microsoft SQL Server** as its database backend.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup for MS SQL Server](#setup-for-ms-sql-server)
   * [Install MS SQL Server](#install-ms-sql-server)
   * [Install `pyodbc` and ODBC Driver](#install-pyodbc-and-odbc-driver)
   * [Configure Database Connection](#configure-database-connection)
   * [Create the Database](#create-the-database)
3. [Running the Application](#running-the-application)
4. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites
* **Python 3.6 or higher**
* **pip** (Python package installer)

---

## 2. Setup for MS SQL Server
This section outlines the steps to set up the application to use a Microsoft SQL Server database.

### 2.1 Install MS SQL Server
If you don't already have MS SQL Server installed:
1. Download MS SQL Server from the official Microsoft website: [MS SQL Server Downloads](https://www.microsoft.com/sql-server/sql-server-downloads).
2. Follow the installation instructions.
3. Make note of the server name, database name, username, and password for later steps.

### 2.2 Install `pyodbc` and ODBC Driver
1. **Install `pyodbc`:**
   Open a terminal or command prompt and run:
   ```bash
   pip install pyodbc
   ```
2. **Install Microsoft ODBC Driver for SQL Server:**
   - Download the appropriate ODBC Driver from Microsoft: [ODBC Driver Downloads](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server).
   - Install the downloaded driver. Note the exact driver name (e.g., `{ODBC Driver 17 for SQL Server}`) for the next step.

### 2.3 Configure Database Connection
1. Open the `database.py` file.
2. Locate the following lines:
   ```python
   DATABASE_CONFIG = {
       'server': 'your_server_name',  # Replace with your server name
       'database': 'your_database_name',  # Replace with your database name
       'username': 'your_username',  # Replace with your username
       'password': 'your_password',  # Replace with your password
   }
   ```
3. Replace the placeholders with your actual SQL Server connection details:
   - `server`: The name or IP address of your SQL Server instance.
   - `database`: The name of the database you want to use for this application.
   - `username`: The username to connect to the SQL server.
   - `password`: The password for the username.

### 2.4 Create the Database
1. **Connect to your SQL Server** using SQL Server Management Studio (SSMS) or another SQL client.
2. **Create the database** if it does not already exist:
   ```sql
   CREATE DATABASE north_sussex_judo;
   GO
   USE north_sussex_judo;
   GO
   ```
3. **Run the schema script:** Use the `north_sussex_judo_schema.sql` file provided in the repository to create the required tables. Execute the script in your SQL client to set up the database schema.

---

## 3. Running the Application
1. Ensure that you have configured the database connection correctly in `database.py`.
2. Navigate to the project directory in your terminal or command prompt:
   ```bash
   cd path/to/your/project
   ```
3. Run the application:
   ```bash
   python main.py
   ```
4. A login window will open. If there are no users in the database, you can create one.
5. Log in and start managing athletes, training plans, competitions, and generating reports.

---

## 4. Troubleshooting
- **Database Connection Errors:** Double-check the database connection details in `database.py` and ensure the database server is running.
- **ODBC Driver Issues:** Verify that the ODBC driver is installed correctly and that the driver name in `database.py` matches exactly.
- **SQL Syntax Errors:** Ensure your SQL queries are compatible with Microsoft SQL Server.
- **Table Does Not Exist:** Ensure that the schema has been applied to the correct database.
- **General Errors:** Check the output and traceback for specific error messages.

---

<a href="https://huggingface.co/Golgrax/GyroUIapk/resolve/main/sample%20video.mkv" style="display: inline-block; padding: 10px 20px; font-size: 16px; text-align: center; text-decoration: none; background-color: #4CAF50; color: white; border-radius: 5px;">Download Sample Video</a>

