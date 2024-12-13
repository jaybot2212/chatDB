import chatDB
import connect
import natural
import time


class SQLLearningSystem:
    def __init__(self):
        self.current_menu = "main"
        self.previous_menus = []
        self.db = connect.chatDB()

    def display_with_delay(self, text: str, delay: float = 0.03, color: str = '\033[1;37m'):
        """Display text progressively with delay and color"""
        print(color, end='')
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print('\033[0m')

    def display_menu_item(self, text: str, color: str = '\033[1;33m'):
        """Display a menu item with color"""
        print(f"{color}{text}\033[0m")
        time.sleep(0.1)

    def display_menu_header(self, text: str):
        """Display a menu header with formatting"""
        # Display the top bar quickly
        print("\n", end='')
        self.display_with_delay("=" * 30, delay=0.005)  # Faster delay for the bar
        # Display the header text
        self.display_with_delay(text, delay=0.01, color='\033[1;36m')  # Slightly faster for the header
        # Display the bottom bar quickly
        self.display_with_delay("=" * 30, delay=0.005)  # Faster delay for the bar
        time.sleep(0.2)  # Adjusted sleep time for smoother experience

    def database_exploration_menu(self):
        while True:
            self.display_menu_header("Database Exploration Options")

            self.display_menu_item("1. View Tables Schema")
            self.display_menu_item("2. View Sample Data")
            self.display_menu_item("\n[B] Back [M] Main Menu [Q] Quit", '\033[1;35m')

            choice = input("\n\033[1;32mEnter your choice: \033[0m").lower()

            if choice == 'b':
                return 'back'
            elif choice == 'm':
                return 'main'
            elif choice == 'q':
                return 'quit'
            elif choice == '1':
                self.display_menu_header("Tables in the Database")

                self.display_with_delay("1. Players Table Schema:", color='\033[1;33m', delay=0.005)
                print(self.db.execute_query('DESCRIBE Players'))
                time.sleep(0.5)

                self.display_with_delay("2. Teams Table Schema:", color='\033[1;33m', delay=0.005)
                print(self.db.execute_query('DESCRIBE Teams'))
                time.sleep(0.5)

                self.display_with_delay("3. Games Table Schema:", color='\033[1;33m', delay=0.005)
                print(self.db.execute_query('DESCRIBE Games'))
                time.sleep(0.5)

                input("\n\033[1;32mPress Enter to continue...\033[0m")

            elif choice == '2':
                self.display_menu_header("Sample Data from Tables")

                self.display_with_delay("1. Players Sample Data:", color='\033[1;33m', delay=0.005)
                print(self.db.execute_query('SELECT * FROM Players LIMIT 5'))
                time.sleep(0.5)

                self.display_with_delay("2. Teams Sample Data:", color='\033[1;33m', delay=0.005)
                print(self.db.execute_query('SELECT * FROM Teams LIMIT 5'))
                time.sleep(0.5)

                self.display_with_delay("3. Games Sample Data:", color='\033[1;33m', delay=0.005)
                print(self.db.execute_query('SELECT * FROM Games LIMIT 5'))
                time.sleep(0.5)

                input("\n\033[1;32mPress Enter to continue...\033[0m")

    def inter_learning(self, command_type: str):
        while True:
            self.display_menu_header("Try Commands Yourself")

            self.display_menu_item("1. Standard SQL Coding")
            self.display_menu_item("2. Natural Language Coding")
            self.display_menu_item("\n[B] Back [M] Main Menu [Q] Quit", '\033[1;35m')

            choice = input("\n\033[1;32mEnter your choice: \033[0m").lower()

            if choice == 'b':
                return 'back'
            elif choice == 'm':
                return 'main'
            elif choice == 'q':
                return 'quit'

            if choice == '1':
                self.display_with_delay("\nYour SQL code will be processed by the MySQL compiler directly",
                                        color='\033[1;36m', delay=0.005)
                while True:
                    user_input = input("\n\033[1;32mPlease enter your SQL query (or 'exit' to quit):\n\033[0m")
                    if user_input.lower() == 'exit':
                        break
                    print(self.db.execute_query(user_input))

            if choice == '2':
                self.display_menu_header("Natural Language to SQL Query Converter")
                self.display_with_delay(f"\nExample queries for {command_type}:", color='\033[1;33m', delay=0.005)

                if command_type == 'SELECT':
                    examples = [
                        "- show all players",
                        "- display the first name and last name of players",
                        "- list the top 5 players by points"
                    ]
                elif command_type == 'WHERE':
                    examples = [
                        "- show players who score more than 20 points",
                        "- find players from team 1",
                        "- display point guards with high rebounds"
                    ]
                elif command_type == 'JOIN':
                    examples = [
                        "- show players with their team names",
                        "- combine players and teams",
                        "- join games with teams"
                    ]
                elif command_type == 'GROUP BY':
                    examples = [
                        "- show average points for each team",
                        "- count players in each position",
                        "- calculate total rebounds by nationality"
                    ]
                elif command_type == 'HAVING':
                    examples = [
                        "- show teams with average points above 20",
                        "- find positions with more than 5 players",
                        "- display teams with total rebounds over 100"
                    ]

                for example in examples:
                    self.display_with_delay(example, delay=0.002)
                    time.sleep(0.05)

                print()  # Add a blank line
                natural.prompt_natural()

    def sql_learning_menu(self):
        while True:
            self.display_menu_header("SQL Learning Options")

            self.display_menu_item("1. Basic SELECT statements")
            self.display_menu_item("2. Filtering with WHERE")
            self.display_menu_item("3. JOIN operations")
            self.display_menu_item("4. GROUP BY and aggregations")
            self.display_menu_item("5. GROUP BY and HAVING")
            self.display_menu_item("\n[B] Back [M] Main Menu [Q] Quit", '\033[1;35m')

            choice = input("\n\033[1;32mEnter your choice: \033[0m").lower()

            if choice == 'b':
                return 'back'
            elif choice == 'm':
                return 'main'
            elif choice == 'q':
                return 'quit'

            elif choice == '1':
                print('\n\033[1;34m=== SELECT Statement ===\033[0m')
                time.sleep(0.3)
                self.display_with_delay('\n[GENERAL EXPLANATION]', color='\033[1;37m', delay=0.005)
                explanations = [
                    'The SELECT command is the fundamental query for retrieving data from a database.',
                    'It allows you to specify exactly which columns you want to see and from which tables.',
                    'This is the most commonly used SQL command and forms the basis of data retrieval.'
                ]
                for line in explanations:
                    self.display_with_delay(line, delay=0.005)
                time.sleep(0.3)

                self.display_with_delay('\n[Key Components]:', color='\033[1;33m', delay=0.005)
                components = [
                    '• Column selection: Choose specific columns or use * for all columns',
                    '• Table specification: Define which table(s) to query from',
                    '• Result limiting: Control the number of returned rows',
                    '• Column aliases: Give readable names to result columns'
                ]
                for component in components:
                    self.display_with_delay(component, delay=0.005)
                    time.sleep(0.1)
                time.sleep(0.3)

                self.display_with_delay('\nExample 1: Basic SELECT', color='\033[1;33m', delay=0.005)
                sample_command = 'SELECT FirstName, LastName, Height_cm FROM Players LIMIT 5'
                self.display_with_delay(f'\nCommand: {sample_command}', color='\033[1;36m', delay=0.005)
                self.display_with_delay('This command selects specific columns from the Players table.', delay=0.005)
                time.sleep(0.3)

                self.display_with_delay('\nResults:', color='\033[1;32m', delay=0.005)
                print(self.db.execute_query(sample_command))
                time.sleep(0.5)

                self.display_with_delay('\nExample 2: SELECT with Column Aliases', color='\033[1;33m', delay=0.005)
                sample_command2 = """
SELECT 
    FirstName as 'First Name',
    LastName as 'Last Name',
    PointsPerGame as 'PPG'
FROM Players 
LIMIT 3"""
                self.display_with_delay(f'\nCommand: {sample_command2.strip()}', color='\033[1;36m', delay=0.005)
                self.display_with_delay('This example shows how to rename columns in the output using aliases.', delay=0.005)
                time.sleep(0.3)

                self.display_with_delay('\nResults:', color='\033[1;32m', delay=0.005)
                print(self.db.execute_query(sample_command2))
                time.sleep(0.5)

                self.display_with_delay('\n[Common Mistakes to Avoid]:', color='\033[1;31m', delay=0.005)
                mistakes = [
                    '• Selecting unnecessary columns',
                    '• Not using LIMIT with large datasets',
                    '• Using SELECT * in production code'
                ]
                for mistake in mistakes:
                    self.display_with_delay(mistake, delay=0.005)
                    time.sleep(0.1)
                time.sleep(1)

                self.inter_learning('SELECT')

            elif choice == '2':
                print('\n\033[1;34m=== WHERE Clause ===\033[0m')
                time.sleep(0.3)
                self.display_with_delay('\n[GENERAL EXPLANATION]', color='\033[1;37m', delay=0.005)
                explanations = [
                    'The WHERE clause filters the result set based on specified conditions.',
                    'It allows you to retrieve only the rows that meet your criteria,',
                    'making it essential for targeted data retrieval and analysis.'
                ]
                for line in explanations:
                    self.display_with_delay(line, delay=0.005)
                time.sleep(0.3)

                self.display_with_delay('\n[Key Components]:', color='\033[1;33m', delay=0.005)
                components = [
                    '• Condition expressions: Define filtering criteria',
                    '• Comparison operators: =, <, >, <=, >=, <>, LIKE, IN',
                    '• Logical operators: AND, OR, NOT',
                    '• Pattern matching: Using LIKE with wildcards'
                ]
                for component in components:
                    self.display_with_delay(component, delay=0.005)
                    time.sleep(0.1)
                time.sleep(0.3)

                self.display_with_delay('\nExample 1: Simple WHERE clause', color='\033[1;33m', delay=0.005)
                sample_command = """
SELECT FirstName, LastName, PointsPerGame 
FROM Players 
WHERE PointsPerGame > 25"""
                self.display_with_delay(f'\nCommand: {sample_command.strip()}', color='\033[1;36m', delay=0.005)
                self.display_with_delay('This finds all high-scoring players (>25 points per game).', delay=0.005)
                time.sleep(0.3)

                self.display_with_delay('\nResults:', color='\033[1;32m', delay=0.005)
                print(self.db.execute_query(sample_command))
                time.sleep(0.5)

                self.display_with_delay('\n[Common Mistakes to Avoid]:', color='\033[1;31m', delay=0.005)
                mistakes = [
                    '• Forgetting to handle NULL values',
                    '• Using wrong comparison operators',
                    '• Not considering data types in comparisons'
                ]
                for mistake in mistakes:
                    self.display_with_delay(mistake, delay=0.005)
                    time.sleep(0.1)
                time.sleep(1)

                self.inter_learning('WHERE')

            elif choice == '3':
                print('\n\033[1;34m=== JOIN Operations ===\033[0m')
                time.sleep(0.3)
                self.display_with_delay('\n[GENERAL EXPLANATION]', color='\033[1;37m', delay=0.005)
                explanations = [
                    'JOIN operations combine rows from two or more tables based on related columns.',
                    'They are crucial for querying related data across multiple tables,',
                    'allowing you to create comprehensive results from normalized databases.'
                ]
                for line in explanations:
                    self.display_with_delay(line, delay=0.005)
                time.sleep(0.3)

                self.display_with_delay('\n[Key Components]:', color='\033[1;33m', delay=0.005)
                components = [
                    '• Join type: INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN',
                    '• Join condition: ON clause specifying the relationship',
                    '• Table aliases: Short names for better readability',
                    '• Multiple joins: Combining more than two tables'
                ]
                for component in components:
                    self.display_with_delay(component, delay=0.005)
                    time.sleep(0.1)
                time.sleep(0.3)

                self.display_with_delay('\nExample 1: Basic INNER JOIN', color='\033[1;33m', delay=0.005)
                sample_command = """
SELECT p.FirstName, p.LastName, t.TeamName 
FROM Players p
JOIN Teams t ON p.TeamID = t.TeamID
LIMIT 5"""
                self.display_with_delay(f'\nCommand: {sample_command.strip()}', color='\033[1;36m', delay=0.005)
                self.display_with_delay('This joins Players and Teams tables to show which team each player belongs to.', delay=0.005)
                time.sleep(0.3)

                self.display_with_delay('\nResults:', color='\033[1;32m', delay=0.005)
                print(self.db.execute_query(sample_command))
                time.sleep(0.5)

                self.display_with_delay('\n[Common Mistakes to Avoid]:', color='\033[1;31m', delay=0.005)
                mistakes = [
                    '• Not specifying join conditions',
                    '• Creating unintended cross joins',
                    '• Forgetting table aliases in complex queries'
                ]
                for mistake in mistakes:
                    self.display_with_delay(mistake, delay=0.005)
                    time.sleep(0.1)
                time.sleep(1)

                self.inter_learning('JOIN')

            elif choice == '4':
                print('\n\033[1;34m=== GROUP BY and Aggregations ===\033[0m')
                time.sleep(0.3)
                self.display_with_delay('\n[GENERAL EXPLANATION]', color='\033[1;37m', delay=0.005)
                explanations = [
                    'GROUP BY groups rows that have the same values in specified columns.',
                    'It is used with aggregate functions to analyze data at a summarized level,',
                    'providing insights about groups rather than individual rows.'
                ]
                for line in explanations:
                    self.display_with_delay(line, delay=0.005)
                time.sleep(0.3)

                self.display_with_delay('\n[Key Components]:', color='\033[1;33m', delay=0.005)
                components = [
                    '• Grouping columns: Columns to group by',
                    '• Aggregate functions: COUNT, SUM, AVG, MAX, MIN',
                    '• Column selection: Must be grouped or aggregated',
                    '• Result ordering: Often used with ORDER BY'
                ]
                for component in components:
                    self.display_with_delay(component, delay=0.005)
                    time.sleep(0.1)
                time.sleep(0.3)

                self.display_with_delay('\nExample 1: Basic Grouping', color='\033[1;33m', delay=0.005)
                sample_command = """
SELECT 
    TeamID,
    COUNT(*) as PlayerCount,
    AVG(PointsPerGame) as AvgPoints
FROM Players
GROUP BY TeamID
LIMIT 5"""
                self.display_with_delay(f'\nCommand: {sample_command.strip()}', color='\033[1;36m', delay=0.005)
                self.display_with_delay('This shows basic grouping with multiple aggregate functions.', delay=0.005)
                time.sleep(0.3)

                self.display_with_delay('\nResults:', color='\033[1;32m', delay=0.005)
                print(self.db.execute_query(sample_command))
                time.sleep(0.5)

                self.display_with_delay('\n[Common Mistakes to Avoid]:', color='\033[1;31m', delay=0.005)
                mistakes = [
                    '• Selecting columns not in GROUP BY',
                    '• Misusing aggregate functions',
                    '• Forgetting to handle NULL values'
                ]
                for mistake in mistakes:
                    self.display_with_delay(mistake, delay=0.005)
                    time.sleep(0.1)
                time.sleep(1)

                self.inter_learning('GROUP BY')

            elif choice == '5':
                print('\n\033[1;34m=== GROUP BY with HAVING ===\033[0m')
                time.sleep(0.3)
                self.display_with_delay('\n[GENERAL EXPLANATION]', color='\033[1;37m', delay=0.005)
                explanations = [
                    'HAVING filters groups created by the GROUP BY clause.',
                    'While WHERE filters individual rows before grouping,',
                    'HAVING filters the groups after GROUP BY is applied,',
                    'allowing you to filter based on aggregate values.'
                ]
                for line in explanations:
                    self.display_with_delay(line, delay=0.005)
                time.sleep(0.3)

                self.display_with_delay('\n[Key Components]:', color='\033[1;33m', delay=0.005)
                components = [
                    '• HAVING conditions: Filters for grouped data',
                    '• Aggregate function conditions: Use COUNT, AVG, etc.',
                    '• Multiple conditions: Can combine with AND/OR',
                    '• Post-grouping filtering: Applied after GROUP BY'
                ]
                for component in components:
                    self.display_with_delay(component, delay=0.005)
                    time.sleep(0.1)
                time.sleep(0.3)

                self.display_with_delay('\nExample 1: Basic HAVING', color='\033[1;33m', delay=0.005)
                sample_command = """
SELECT 
    TeamID,
    COUNT(*) as PlayerCount,
    AVG(PointsPerGame) as AvgPoints
FROM Players
GROUP BY TeamID
HAVING AVG(PointsPerGame) > 20"""
                self.display_with_delay(f'\nCommand: {sample_command.strip()}', color='\033[1;36m', delay=0.005)
                self.display_with_delay('This shows teams averaging more than 20 points per player.', delay=0.005)
                time.sleep(0.3)

                self.display_with_delay('\nResults:', color='\033[1;32m', delay=0.005)
                print(self.db.execute_query(sample_command))
                time.sleep(0.5)

                self.display_with_delay('\n[Common Mistakes to Avoid]:', color='\033[1;31m', delay=0.005)
                mistakes = [
                    '• Using WHERE instead of HAVING for aggregates',
                    '• Incorrect aggregate function usage',
                    '• Not understanding WHERE vs HAVING'
                ]
                for mistake in mistakes:
                    self.display_with_delay(mistake, delay=0.005)
                    time.sleep(0.1)
                time.sleep(1)

                self.inter_learning('HAVING')

            else:
                print("\n\033[1;31mInvalid choice. Please try again.\033[0m")

    def main_menu(self):
        while True:
            self.display_menu_header("SQL Learning System")
            self.display_with_delay(f"Current Location: {self.current_menu.upper()}",
                                    color='\033[1;36m', delay=0.005)

            self.display_menu_item("\nMain Menu Options:")
            self.display_menu_item("1. Database Exploration")
            self.display_menu_item("2. SQL Commands Learning")

            if self.previous_menus:
                self.display_menu_item("\n[B] Back [Q] Quit", '\033[1;35m')
            else:
                self.display_menu_item("\n[Q] Quit", '\033[1;35m')

            choice = input("\n\033[1;32mEnter your choice: \033[0m").lower()

            if choice == 'q':
                return 'quit'
            elif choice == 'b' and self.previous_menus:
                self.current_menu = self.previous_menus.pop()
                continue

            self.previous_menus.append(self.current_menu)

            if choice == '1':
                self.current_menu = "database exploration"
                result = self.database_exploration_menu()
            elif choice == '2':
                self.current_menu = "sql learning"
                result = self.sql_learning_menu()
            else:
                continue

            if result == 'quit':
                return 'quit'
            elif result == 'main':
                self.current_menu = "main"
                self.previous_menus = []
            elif result == 'back':
                if self.previous_menus:
                    self.current_menu = self.previous_menus.pop()

    def run(self):
        try:
            while True:
                result = self.main_menu()
                if result == 'quit':
                    self.display_with_delay("\nThank you for using the SQL Learning System! Goodbye!",
                                            color='\033[1;36m', delay=0.005)
                    break
        except KeyboardInterrupt:
            self.display_with_delay("\n\nProgram terminated by user. Goodbye!",
                                    color='\033[1;31m', delay=0.005)
        except Exception as e:
            self.display_with_delay(f"\nAn error occurred: {str(e)}", color='\033[1;31m', delay=0.005)


if __name__ == "__main__":
    chatDB.print_welcome()
    learning_system = SQLLearningSystem()
    learning_system.run()
