# E-commerce Data Engineering Pipeline

An end-to-end data engineering project that extracts, cleans, validates, transforms and loads e-commerce data into a MySQL data warehouse using Python and SQL.

The project demonstrates an automated ETL workflow, relational database design, dimensional modelling, data quality checks, pipeline logging and automated testing.

## Project Overview

This project simulates an e-commerce business that needs to process customer, product and order data for reporting and analysis.

The pipeline takes raw CSV data, cleans and validates it, loads it into a MySQL source database, and transforms it into a separate data warehouse designed using a star schema.

The final warehouse is structured to support business intelligence and analytical reporting.

## Architecture

The pipeline follows this execution sequence:

1. Create the source MySQL database.
2. Create the data warehouse and its tables.
3. Clean raw order data.
4. Validate data quality.
5. Load cleaned data into the source database.
6. Populate the date dimension.
7. Load dimensions and sales facts into the warehouse.

### Data Flow

`CSV Files → Python ETL → Data Cleaning → Data Validation → MySQL Source Database → Data Warehouse → Business Intelligence`

## Technologies Used

- **Python** – ETL development and pipeline orchestration.
- **Pandas** – Data manipulation and transformation.
- **MySQL** – Relational database and data warehouse.
- **SQL** – Database creation, queries and analytical transformations.
- **Pytest** – Automated testing.
- **Python Logging** – Pipeline execution monitoring.
- **Git and GitHub** – Version control and project hosting.

## Data Warehouse Design

The project uses a star schema consisting of four tables:

| Table | Description |
|---|---|
| `fact_sales` | Stores sales transactions and measures |
| `dim_customer` | Stores customer information |
| `dim_product` | Stores product information |
| `dim_date` | Stores calendar and date attributes |

The fact table connects to the three dimension tables through foreign keys.

This design makes it easier to analyse sales by customer, product and date.

## Data Cleaning and Quality

The cleaning process handles:

- Duplicate order records.
- Orders with unknown customers.
- Orders with zero or negative quantities.
- Separation of valid and rejected records.

The original sample contained 11 order records. After cleaning, 7 valid records were retained and 3 rejected. One duplicate record was removed.

## Key Results

The current sample dataset produces the following results:

| Metric | Result |
|---|---:|
| Valid orders loaded | 7 |
| Units sold | 15 |
| Total sales revenue | R2,439.85 |
| Average order value | R348.55 |
| Customers | 6 |
| Products | 5 |

These figures are calculated from the current sample data and are not intended to represent a real business.

## Project Structure

```text
ecommerce-data-pipeline/
│
├── data/
│   ├── customers.csv
│   ├── orders.csv
│   ├── products.csv
│   └── processed/
│       ├── clean_orders.csv
│       └── rejected_orders.csv
│
├── sql/
│   ├── sales_analysis.sql
│   ├── analytics/
│   │   ├── customer_revenue.sql
│   │   ├── inactive_customers.sql
│   │   └── product_revenue.sql
│   └── warehouse/
│       └── schema.sql
│
├── src/
│   ├── clean_data.py
│   ├── create_database.py
│   ├── create_warehouse.py
│   ├── load_data.py
│   ├── load_dates.py
│   ├── load_warehouse.py
│   ├── profile_data.py
│   ├── run_pipeline.py
│   ├── schema.sql
│   ├── test_connection.py
│   └── validate_data.py
│
├── tests/
│   ├── test_clean_data.py
│   ├── test_load_data.py
│   └── test_load_warehouse.py
│
├── logs/
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/nasirahmohamud-ai/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure database credentials

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=ecommerce_dw
```

Replace `your_mysql_password` with your own MySQL password.

Keep `.env` private and never commit it to GitHub.

### 5. Run the pipeline

Make sure your MySQL server is running, then execute:

```powershell
python .\src\run_pipeline.py
```

The pipeline automatically creates the source database and warehouse tables, processes the data and loads the warehouse.

Execution logs are recorded in:

```text
logs/pipeline.log
```

## Running Automated Tests

Run the complete test suite:

```powershell
python -m pytest -v
```

The project currently has **13 passing automated tests** covering data cleaning, source database loading and warehouse loading.

The warehouse loader tests use mocked database operations, so they do not require a live MySQL connection.

## Future Improvements

Potential future enhancements include:

- Building a Power BI dashboard connected to the data warehouse.
- Adding larger and more realistic datasets.
- Improving pipeline error handling and monitoring.
- Containerising the application using Docker.
- Deploying the pipeline to a cloud environment.
- Introducing a dedicated workflow orchestration tool.

## Author

**Nasirah Mohamud**

Aspiring Data Engineer

GitHub: [nasirahmohamud-ai](https://github.com/nasirahmohamud-ai)

---

*This project was developed as a hands-on learning and portfolio project to demonstrate practical data engineering skills.*
