import mysql.connector
from tabulate import tabulate


class chatDB:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect_to_db()

    def connect_to_db(self):
        """Connect to local MySQl database"""
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="jasonhu",
                password="hxh117221",
                database="ChatDB")
            self.cursor = self.connection.cursor()
            print("Successfully connected to NBA database")
        except mysql.connector.Error as err:
            print("Connection Failed")

    def execute_query(self, query):
        """Send Query"""
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            # Extract column names for tabular format
            column_names = [desc[0] for desc in self.cursor.description]

            # Format the output using tabulate
            formatted_output = tabulate(results, headers=column_names, tablefmt="psql")
            return formatted_output
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return None


if __name__ == "__main__":
    db = chatDB()
    print(db.execute_query('SELECT * FROM Players LIMIT 1'))
