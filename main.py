from sql_functions import SQLFunctions
from database_setup import get_engine

def main():
    """
    run this file to update all ETFs
    """
    # list of ETFs to track and update (dummy data)
    ETFs = ['GLD', 'SPY', 'QQQ', 'TLT', 'IWM', 'GDX', 'SLV', 'SMH', 'USO']

    #create engine to connect
    engine = get_engine()

    for etf in ETFs:
        print(f'====== {etf} ======')
        SQLFunctions.import_to_sql(symbol=etf, engine=engine)
        SQLFunctions.export_to_csv(symbol=etf, engine=engine)

    engine.dispose()


if __name__ == '__main__':
    main()
