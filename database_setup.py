from sqlalchemy import create_engine

def get_engine():
    engine = create_engine('sqlite:///etf_data.db', echo=False)  # Use echo=True for debugging SQL statements
    return engine
