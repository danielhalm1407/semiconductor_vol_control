from sqlalchemy import create_engine
from sqlalchemy import inspect, text
import logging
import os
import sys

#Getting the engine

logging.info('Finding current Path')
__file__ = "sql_queries.py"
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(current_dir, '..'))



def get_sql_engine(data_path):
    """
    Returns a SQLAlchemy engine object for connecting to a SQLite database.

    If the engine object has not been created yet, it will be created and stored
    as a static attribute of the `get_sql_engine` function.

    Returns:
        sqlalchemy.engine.Engine: The SQLAlchemy engine object.
    """
    if not hasattr(get_sql_engine, 'engine'):
        get_sql_engine.engine = create_engine('sqlite:///' + data_path)
    return get_sql_engine.engine



# Create a table with Pandas
def make_table(df, name, engine, if_exists='append'):
    with engine.connect() as conn:
        pass
    df.to_sql(name, engine, if_exists=if_exists, index=False)

#SQL QUERIES
DROP_TABLE_SQL_QUERY = "DROP TABLE IF EXISTS bloomberg_rankings;"