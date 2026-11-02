
# E-commerce Data Pipeline

## Project Overview

This project is an end-to-end data pipeline built using Python, MySQL and SQL.

It processes raw e-commerce data, cleans and validates records, and loads the resulting data into a MySQL database for analysis.

The project demonstrates fundamental data engineering concepts, including data cleaning, data validation, database management, pipeline orchestration, logging and SQL analytics.

## Technologies Used

- Python
- MySQL
- SQL
- Pandas
- MySQL Connector/Python
- Pytest
- Git and GitHub


## Pipeline Workflow

The pipeline follows these stages:

1. **Database Setup** – Creates the MySQL database and tables if they do not already exist.
2. **Data Cleaning** – Removes exact duplicate records and separates invalid orders from valid records.
3. **Data Validation** – Checks for missing values, duplicate order IDs, invalid quantities and missing dates.
4. **Data Loading** – Loads customers, products and valid orders into MySQL.
5. **SQL Analytics** – Uses SQL queries to analyse product revenue, customer spending and inactive customers.

## Project Structure

```text
ecommerce-data-pipeline/
│
├── data/
│   ├── processed/
│   ├── customers.csv
│   ├── products.csv
│   └── orders.csv
│
├── logs/
│   └── pipeline.log
│
├── src/
│   ├── create_database.py
│   ├── clean_data.py
│   ├── validate_data.py
│   ├── load_data.py
│   ├── run_pipeline.py
│   └── schema.sql
│
├── sql/
│   └── analytics/
│       ├── customer_revenue.sql
│       ├── product_revenue.sql
│       └── inactive_customers.sql
│
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd ecommerce-data-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root directory.

Add your MySQL connection settings:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=ecommerce_dw
```

Replace `your_mysql_password` with your own MySQL password.

**Security:** Never upload your `.env` file or database password to GitHub.

### 6. Run the pipeline

```bash
python src/run_pipeline.py
```

## SQL Analytics

The project includes SQL queries stored in `sql/analytics/`:

| SQL File | Purpose |
|---|---|
| `product_revenue.sql` | Calculates revenue and items sold per product. |
| `customer_revenue.sql` | Analyses customer spending and order counts. |
| `inactive_customers.sql` | Identifies customers who have not placed orders. |

These queries demonstrate SQL aggregation, joins, grouping, sorting and filtering.

## Data Quality and Testing

The project includes automated tests using Pytest.

The tests cover:

- Data cleaning and duplicate removal.
- Validation of cleaned order records.
- Customer, product and order loading functions.
- Duplicate update SQL statement handling.

Run the tests using:

```bash
python -m pytest -v
```

## Current Project Results

The sample dataset contains:

| Metric | Result |
|---|---:|
| Customers loaded | 6 |
| Products loaded | 5 |
| Valid orders loaded | 7 |
| Rejected orders | 3 |
| Total items sold | 15 |
| Total revenue | R2,439.85 |

The pipeline successfully cleans, validates and loads the sample data into MySQL.


## Future Improvements

Potential future enhancements include:

- Automating pipeline execution on a scheduled basis.
- Adding more advanced data quality checks.
- Expanding SQL analytics and reporting.
- Building a Power BI dashboard using the loaded data.
- Implementing more comprehensive database integration tests.
- Improving pipeline monitoring and error reporting.
