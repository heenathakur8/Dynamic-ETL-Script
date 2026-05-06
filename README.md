 🚀 Dynamic ETL Pipeline: MySQL → ClickHouse Cloud

 📌 Overview

This project implements a fully dynamic ETL (Extract, Transform, Load) pipeline using Python.
It extracts data from a MySQL database, applies transformations, and loads it into ClickHouse Cloud for high-performance analytics.

---

 🧠 Key Features

* 🔄 Dynamic Table Extraction – Automatically detects and processes all tables from MySQL
* 🧩 Schema Inference – Dynamically maps MySQL/Pandas data types to ClickHouse schema
* ⚡ Chunk-Based Processing – Efficient handling of large datasets
* ☁️ Cloud Integration – Loads data into ClickHouse Cloud
* 🔐 Secure Configuration – Uses `.env` for credentials (no hardcoding)

---

 🏗️ Tech Stack

* Python
* Pandas
* PyMySQL
* ClickHouse Connect
* dotenv


 ⚙️ Setup Instructions

 1. Clone the repository

bash
git clone https://github.com/your-username/etl-clickhouse-pipeline.git
cd etl-clickhouse-pipeline


---

 2. Install dependencies

bash
pip install -r requirements.txt


---

 3. Configure environment variables

Create a `.env` file:

env
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=your_database

CH_HOST=your-clickhouse-host
CH_USER=default
CH_PASSWORD=your-password
CH_DATABASE=default


---

 4. Run the ETL pipeline

bash
python etl.py


---

 🔄 ETL Workflow

1. Extract

   * Connects to MySQL
   * Fetches all tables dynamically

2. Transform

   * Removes duplicates
   * Handles missing values
   * Converts data types (important for ClickHouse compatibility)

3. Load

   * Dynamically creates tables in ClickHouse
   * Inserts data using optimized batch processing

---

 🧪 Example Query (ClickHouse)

sql
SELECT count(*) FROM products;


---

 🚨 Challenges Solved

* Handling `numpy` vs native Python types
* Dynamic schema generation for heterogeneous tables
* DateTime conversion issues with ClickHouse
* Efficient bulk insertion

---
