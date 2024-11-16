from math import e
import os
import pandas as pd
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine

class Database:
    def __init__(self, db_name: str = 'database'):
        self.engine = create_engine(f"sqlite:///{db_name}.db")
        
    def dataframe_to_table(self, df: pd.DataFrame, table_name: str):
        df.to_sql(table_name, self.engine, index=True, if_exists='replace')
    
    def read(self, path: str, name: str):
        if name.endswith('.csv'):
            df = pd.read_csv(path)
        elif name.endswith('.xlsx') or name.endswith('.xls'):
            df = pd.read_excel(path)
        elif name.endswith('.parquet'):
            df = pd.read_parquet(path)
        else:
            raise ValueError("Unsupported file format")
        table_name = name.split('.')[0]
        self.dataframe_to_table(df, table_name)
        
    def get_sql_database(self, ):
        return SQLDatabase(engine=self.engine)

    def drop_database(self, db_name: str = 'database'):
        try:
            os.remove(f"{db_name}.db")
        except FileNotFoundError:
            print(f"{db_name}.db not found")