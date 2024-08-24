import sys
import os
import logging
import pandas as pd

def get_user_input(prompt):
    user_input = input(prompt).strip().lower().replace(' ', '_')
    return user_input if user_input else 'table_1'
        
#__file__ = "sql_in.py"
def main():
    logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(filename)s] %(message)s', level=logging.INFO)
    logging.getLogger().setLevel(logging.INFO)
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        current_dir = os.getcwd()  # __file__ is not defined in interactive mode

        # Print the current directory
        print(f'Current Directory: {current_dir}')

    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
        print(f'Inserting Parent Path: {parent_dir}')

    # Print the updated sys.path
        print(f'Priority System Path: {sys.path[0]}')
    try:
        import econ_utils
        from econ_utils import sql_queries as sqlq
        print('Successfully imported sql_queries as sqlq from econ_utils')
    except ImportError as e:
        print(f'Error importing econ_utils: {e}')
        sys.exit(1)

    # THE MAIN SCRIPT
    logging.info('Retrieving the bloomberg dataframe')
    bloomberg_data = pd.read_excel(os.path.join(sys.path[0],"../data/bloomberg_data.xlsx"))
    logging.info('bloomberg dataframe retreived')

    logging.info('Retrieving the Database/Creating if not Existing Already')
    engine = sqlq.get_sql_engine()
    logging.info('Retrieved the Database')

    # Create an inspector object
    inspector = sqlq.inspect(sqlq.engine)

    # Get a list of all table names
    tables = inspector.get_table_names()

    name = get_user_input("What do you want to call the table?")
    if_exists = 'append'
    if name in tables:
        replace = input(f'Table name: {name} already exists. Replace? (Else will append to the table) [Y/N] ').strip().lower().replace(' ', '_')
        if replace == 'y':
            if_exists = 'replace'

    print(f'Your data will be saved to the table name: {name}')
    sqlq.make_table(df = bloomberg_data, name = name, engine = engine, if_exists=if_exists)
    
    logging.info('Saved a table to database')

if __name__ == "__main__":
    print("Script is being run directly")
    main()
else:
    print("Script is being imported")