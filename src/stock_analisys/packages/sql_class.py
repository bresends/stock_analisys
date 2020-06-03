"""
SQL Object For Handlilng SQL Filling  
"""

from sqlalchemy import create_engine


class MySQL:
    def __init__(self, database="stocks"):
        self.database = database
        self.stocks_db_engine = create_engine(
            f"mysql+mysqlconnector://root:74Q50c$0rIZ&GDhp@localhost:3306/{database}",
            echo=False,
        )

    def update(self, table, changed_column, value, where_column, where_equals):

        """
        MySQL update
        """
        self.stocks_db_engine.execute(
            f"""UPDATE {self.database}.{table} SET {changed_column} = '{value}' WHERE ({where_column} = '{where_equals}') LIMIT 1;"""
        )
    
    def select_unique_column(self, table, desired_column, where_column, where_equals):
        """Grabs a sing column from an SQL table

        Arguments:
            table -- Desired Table to Analyse
            desired_column -- Column that you wish to bring inside python
            where_column -- Column that you will use as a control for the query 
            where_equals -- The value you wish to use as control 

        Returns:
            tuple -- returns the first element of the result tuple query 
        """
        query_response = self.stocks_db_engine.execute(f"SELECT {desired_column} FROM {table} WHERE {where_column} = '{where_equals}' LIMIT 0, 5000;")
        result = tuple(x[0] for x in query_response.fetchall())
        return result


    def __str__(self):
        return f"MySQL(database = ('{self.database}')"


def update_test():
    sql_handler = MySQL()

    sql_handler.update(
        table="company_info",
        changed_column="origin",
        value="United States of America",
        where_column="ticker",
        where_equals="A",
    )

def single_column_select_test():
    sql_handler = MySQL()

    result = sql_handler.select_unique_column(
        table="company_info",
        desired_column="ticker",
        where_column="origin",
        where_equals="{{inc-country}}",
    )

    print(result)


if __name__ == "__main__":
    # update_test()
    single_column_select_test()

    
