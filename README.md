# etf-sql-database
An efficientl ETF database management system. when run ,recent  data for specific tickers are stored in the SQLite file etf_data. This avoids reaching API limits. Prices are also adjusted using the adjustment ratio to prep data for backtesting


## Start
1. **Clone the Repository**:
   ```
   git clone https://github.com/left-nullspace/etf-sql-database-python
   ```
2. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```
3. **Run the Application**:
   ```
   python main.py
   ```

## Features
- **Efficient Data Fetching**: Updates only new data from Yahoo Finance.
- **Data Adjustment**: Adjusts OHLC data for accurate backtesting.
- **CSV Export**: Exports data to CSV format.

## Directory Structure
- `csv_data/`: Stores exported CSV files.
- `database_setup.py`: Sets up the database connection.
- `main.py`: Main script to update and export data.
- `sql_functions.py`: Handles SQL operations.
- `SQL_Querying.ipynb`: Demonstrates SQL queries on the data.
