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

    def __str__(self):
        return f"MySQL(database = ('{self.database}')"


def main():
    sql_handler = MySQL()

    sql_handler.update(
        table="company_info",
        changed_column="origin",
        value="United States of America",
        where_column="ticker",
        where_equals="A",
    )


if __name__ == "__main__":
    main()
