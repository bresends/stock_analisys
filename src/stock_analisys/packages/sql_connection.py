"""
Inserts data into MySql Database 
"""

import pandas as pd
import sqlalchemy as sql
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey

# Define the MySQL engine using MySQL Connector/Python
connect_stocks_database = (
    "mysql+mysqlconnector://root:74Q50c$0rIZ&GDhp@localhost:3306/stocks"
)
sql_engine = sql.create_engine(connect_stocks_database, echo=False)
