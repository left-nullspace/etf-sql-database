import os
import pandas as pd
import yfinance as yf
from database_setup import get_engine
from datetime import datetime

class SQLFunctions:
    
    @staticmethod
    def _adjust_prices(df):
        """
        - adjust ohlc prices according to the AdjClose/Close ratio
        - factors in 
        """
        adjustment_factor = df['Adj Close'] / df['Close']
        df['Open'] = df['Open'] * adjustment_factor
        df['High'] = df['High'] * adjustment_factor
        df['Low'] = df['Low'] * adjustment_factor
        df['Close'] = df['Adj Close']  # Using adjusted close as the new close
        return df

    @staticmethod
    def import_to_sql(symbol, engine):
        """
        try to append the data if table exists, if not create table for ticker
        """
        
        start='1950-01-01' #date to start pulling data from
        
        try:
            # try to append the data
            query = f'SELECT MAX(Date) FROM "{symbol}"'
            max_date_result = pd.read_sql(query, engine)
            if max_date_result.empty or max_date_result.iloc[0, 0] is None:
                raise ValueError(f"No data found for {symbol}. Likely table does not exist.")

            max_date = pd.to_datetime(max_date_result['MAX(Date)'][0])
            print(f'Max date found: {max_date}')

            # check if the max date is today, if yes, skip fetching new data
            if max_date >= pd.to_datetime(datetime.now().date()):
                print(f"No new data to fetch for {symbol}. Last update is current.")
                return
            
            # Pull data from this max date onward
            new_data = yf.download(symbol, start=max_date)
            new_data.reset_index(inplace=True)
            new_data = SQLFunctions._adjust_prices(new_data)  # Adjusted to call the private method
            new_rows = new_data[new_data['Date'] > max_date]

            # Append it to the existing SQL table
            new_rows.to_sql(symbol, engine, if_exists='append', index=False)
            print(f'{len(new_rows)} new rows added to {symbol}')

        except Exception as e:      #IF TABLE DOESNT EXIST
            print(f"Error encountered, the table likely doesnt exist ")
            #print(e)

            # if table does not exist, create it
            new_data = yf.download(symbol, start=start)
            new_data.reset_index(inplace=True)
            new_data = SQLFunctions._adjust_prices(new_data)  # Adjusted to call the private method
            new_data.to_sql(symbol, engine, if_exists='replace', index=False)
            print(f'New table created for {symbol} with {len(new_data)} rows')


    @staticmethod
    def export_to_csv(symbol, engine):
        
        # export the table to a CSV file
        query = f"SELECT * FROM \"{symbol}\""
        df = pd.read_sql(query, con=engine)
        df.to_csv(f'csv_data/{symbol}.csv', index=False)
        print(f'Table {symbol} exported to csv_data/{symbol}.csv')