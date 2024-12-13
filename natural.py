import re
import connect


def detect_aggregates(input_lower: str, col: str, command_patterns: dict) -> list:
    """Helper function to detect and format aggregate functions."""
    aggregates = []
    input_tokens = set(input_lower.split())
    for command in ['count', 'average', 'sum', 'maximum', 'minimum']:
        if input_tokens.intersection(command_patterns[command]):
            if command == 'count':
                aggregates.append(f"COUNT(*) as count")
            elif command == 'average':
                aggregates.append(f"AVG({col}) as {col}_avg")
            elif command == 'sum':
                aggregates.append(f"SUM({col}) as {col}_sum")
            elif command == 'maximum':
                aggregates.append(f"MAX({col}) as {col}_max")
            elif command == 'minimum':
                aggregates.append(f"MIN({col}) as {col}_min")
    return aggregates


def extract_top_n_phrase(input_lower):
    """
    Extracts the 'top N' phrase and returns the number N and the column to order by.
    """
    match = re.search(r'(?:top\s+(\d+)\s*([\w\s]+)?|([\w\s]+)\s+top\s+(\d+))', input_lower)
    if match:
        if match.group(1):  # Matches 'top N [column]'
            n = int(match.group(1))
            column_phrase = match.group(2)
        else:  # Matches '[column] top N'
            n = int(match.group(4))
            column_phrase = match.group(3)
        return n, column_phrase.strip() if column_phrase else None
    return None, None


def parse_conditions(input_lower: str, table_schema: dict, comparison_patterns: dict, comparison_patterns_map: dict,
                     aggregate_columns: list, used_numbers: set) -> dict:
    """
    Parse the input to find conditions for the WHERE and HAVING clauses.
    Returns a dict with 'where' and 'having' keys.
    This improved version attempts to correctly identify columns and operators.
    """
    conditions = {'where': [], 'having': []}

    # We will split the input into clauses based on known logical connectors
    clauses = re.split(r',| and | or ', input_lower)
    clauses = [c.strip() for c in clauses if c.strip()]

    for clause in clauses:
        # Attempt to find a comparison operator pattern in the clause
        found_operator = None
        for comp, patterns in comparison_patterns.items():
            for pattern in patterns:
                if pattern in clause:
                    found_operator = (comp, comparison_patterns_map[comp], pattern)
                    break
            if found_operator:
                break

        # If we don't find an operator, move on
        if not found_operator:
            continue

        # Extract numeric value if present
        numeric_match = re.search(r'\b\d+(\.\d+)?\b', clause)
        found_value = numeric_match.group() if numeric_match else None

        # If we have an operator but no numeric value, we might skip.
        # (Advanced logic can be implemented here if needed.)
        if not found_value:
            # No numeric value found. We can attempt a fallback or skip.
            continue

        # Identify all possible columns in the clause
        possible_columns = []
        for col, col_info in table_schema['columns'].items():
            col_aliases = [col.lower()] + col_info['aliases']
            for alias in col_aliases:
                pos = clause.find(alias)
                if pos != -1:
                    possible_columns.append((col, pos, col_info['type']))

        if not possible_columns:
            # No columns found in this clause; skip
            continue

        # Choose the best column:
        # Heuristic: pick the column that appears before the operator phrase and is suitable type-wise
        # We'll find where the operator pattern is located in the clause.
        operator_text = found_operator[2]
        op_pos = clause.find(operator_text)

        # Filter columns that appear before the operator (this often makes sense, e.g. "height under 200")
        # If none appear before, we just pick the first column encountered.
        numeric_compare_ops = ['>', '<', '>=', '<=', '!=', '=']
        best_col = None
        if found_operator[1] in numeric_compare_ops and found_value:
            # Prefer numeric columns if numeric operation
            numeric_columns = [c for c in possible_columns if c[2] in ['int', 'float']]
            if numeric_columns:
                # Among numeric columns, pick one closest to operator
                numeric_columns.sort(key=lambda x: abs(x[1] - op_pos))
                best_col = numeric_columns[0][0]
            else:
                # No numeric columns, pick closest column to operator anyway
                possible_columns.sort(key=lambda x: abs(x[1] - op_pos))
                best_col = possible_columns[0][0]
        else:
            # Not a numeric compare or no numeric value
            # Just pick closest column to operator
            possible_columns.sort(key=lambda x: abs(x[1] - op_pos))
            best_col = possible_columns[0][0]

        # Now we have a column, operator and value
        sql_operator = found_operator[1]
        # Check if the column is involved in aggregation
        # NOTE: In this simple approach, we do not map conditions to aggregates directly.
        # If needed, detect if column is part of aggregate_columns and adjust condition for HAVING.
        if best_col in [agg_col.split('(')[-1].split(')')[0] for agg_col in aggregate_columns]:
            # Condition on an aggregated column:
            # Identify which aggregator applies to this column
            # We assume only one aggregator per column for simplicity
            agg_to_use = None
            for agg_col_expr in aggregate_columns:
                col_in_agg = agg_col_expr.split('(')[-1].split(')')[0]
                if col_in_agg == best_col:
                    # Extract aggregator name from agg_col_expr, e.g. AVG(col)
                    agg_to_use = agg_col_expr.split('(')[0].strip()
                    agg_to_use = agg_to_use.split()[-1]  # e.g. from "AVG(col) as col_avg" get "AVG"
                    break

            if agg_to_use:
                condition = f"{agg_to_use}({best_col}) {sql_operator} {found_value}"
                conditions['having'].append(condition)
            else:
                condition = f"{best_col} {sql_operator} {found_value}"
                conditions['where'].append(condition)
        else:
            # Normal column condition
            condition = f"{best_col} {sql_operator} {found_value}"
            conditions['where'].append(condition)

    return conditions


def natural_language_to_sql(user_input: str) -> tuple:
    """
    Convert natural language input to SQL query using pattern matching.
    """
    command_patterns = {
        'select': ['select', 'get', 'show', 'display', 'find', 'choose', 'pick', 'what', 'list'],
        'join': ['join', 'combine', 'relate', 'with'],
        'group': ['group', 'cluster', 'categorize', 'group by', 'per'],
        'order': ['order', 'sort', 'arrange', 'rank', 'by'],
        'count': ['count', 'how many', 'number of', 'total'],
        'sum': ['sum', 'total'],
        'average': ['average', 'mean', 'avg'],
        'maximum': ['maximum', 'highest', 'most', 'max', 'greatest', 'biggest'],
        'minimum': ['minimum', 'lowest', 'least', 'min', 'smallest'],
        'limit': ['only', 'just', 'limit', 'top', 'first', 'under', 'at most'],
        'desc': ['desc', 'descending', 'decreasing', 'high to low', 'largest to smallest', 'biggest to smallest'],
        'asc': ['asc', 'ascending', 'increasing', 'low to high', 'smallest to largest'],
        'having': ['having', 'with', 'that have', 'whose'],
        'where': ['where', 'filter'],
        'and': ['and', 'as well as'],
        'or': ['or'],
        'not': ['not', 'no', 'without']
    }

    comparison_patterns = {
        'greater_than': ['greater than', 'more than', 'above', 'exceeding', 'over', 'taller than', 'heavier than',
                         'older than', 'after'],
        'less_than': ['less than', 'fewer than', 'below', 'under', 'smaller than', 'lighter than', 'younger than',
                      'before'],
        'equal_to': ['equal to', 'equals', 'equal', 'is', 'are', 'was', 'were'],
        'not_equal_to': ['not equal to', 'not equals', 'not equal', 'is not', 'are not', 'was not', 'were not',
                         'does not equal', "isn't", "aren't"],
        'greater_or_equal': ['at least', 'no less than', 'greater than or equal to', 'minimum', 'not less than'],
        'less_or_equal': ['at most', 'no more than', 'less than or equal to', 'maximum', 'not greater than']
    }

    comparison_patterns_map = {
        'greater_than': '>',
        'less_than': '<',
        'equal_to': '=',
        'not_equal_to': '!=',
        'greater_or_equal': '>=',
        'less_or_equal': '<='
    }

    table_relationships = {
        ('Players', 'Teams'): ('TeamID', 'TeamID'),
        ('Teams', 'Players'): ('TeamID', 'TeamID'),
        ('Games', 'Teams'): ('HomeTeamID', 'TeamID'),
        ('Teams', 'Games'): ('TeamID', 'HomeTeamID'),
        ('Games', 'Players'): ('PlayerID', 'PlayerID'),
        ('Players', 'Games'): ('PlayerID', 'PlayerID')
    }

    schemas = {
        'Players': {
            'columns': {
                'PlayerID': {'aliases': ['playerid', 'player id', 'id'], 'type': 'int'},
                'FirstName': {'aliases': ['firstname', 'first name', 'name'], 'type': 'string'},
                'LastName': {'aliases': ['lastname', 'last name', 'surname'], 'type': 'string'},
                'Position': {'aliases': ['position', 'pos', 'role'], 'type': 'string'},
                'TeamID': {'aliases': ['teamid', 'team id'], 'type': 'int'},
                'Height_cm': {'aliases': ['height', 'height_cm', 'tall'], 'type': 'float'},
                'Weight_kg': {'aliases': ['weight', 'weight_kg'], 'type': 'float'},
                'Birthdate': {'aliases': ['birthdate', 'birth', 'dob', 'born'], 'type': 'date'},
                'Nationality': {'aliases': ['nationality', 'nation', 'country'], 'type': 'string'},
                'PointsPerGame': {'aliases': ['points', 'ppg', 'scoring', 'pointspergame'], 'type': 'float'},
                'ReboundsPerGame': {'aliases': ['rebounds', 'rpg', 'reboundspergame'], 'type': 'float'},
                'AssistsPerGame': {'aliases': ['assists', 'apg', 'assistspergame'], 'type': 'float'},
                'StealsPerGame': {'aliases': ['steals', 'spg', 'stealspergame'], 'type': 'float'},
                'BlocksPerGame': {'aliases': ['blocks', 'bpg', 'blockspergame'], 'type': 'float'},
                'NetWorth_USD': {'aliases': ['networth', 'worth', 'value'], 'type': 'float'}
            },
            'aliases': ['player', 'players', 'roster']
        },
        'Teams': {
            'columns': {
                'TeamID': {'aliases': ['teamid', 'team id'], 'type': 'int'},
                'TeamName': {'aliases': ['teamname', 'team name', 'name'], 'type': 'string'},
                'CEO': {'aliases': ['ceo', 'chief executive'], 'type': 'string'},
                'Owner': {'aliases': ['owner', 'owned by'], 'type': 'string'},
                'Location': {'aliases': ['location', 'city', 'place'], 'type': 'string'},
                'Stadium': {'aliases': ['stadium', 'arena', 'court'], 'type': 'string'},
                'FoundedYear': {'aliases': ['founded', 'established', 'foundedyear'], 'type': 'int'},
                'NetWorth_USD': {'aliases': ['networth', 'worth', 'value'], 'type': 'float'}
            },
            'aliases': ['team', 'teams', 'franchise', 'franchises']
        },
        'Games': {
            'columns': {
                'GameID': {'aliases': ['gameid', 'game id', 'match id'], 'type': 'int'},
                'HomeTeamID': {'aliases': ['hometeamid', 'home team id', 'home', 'hometeam'], 'type': 'int'},
                'GuestTeamID': {'aliases': ['guestteamid', 'guest team id', 'away team id', 'visitor'], 'type': 'int'},
                'Time': {'aliases': ['time', 'date', 'when'], 'type': 'date'},
                'Score': {'aliases': ['score', 'result', 'points'], 'type': 'int'},
                'Round': {'aliases': ['round', 'stage'], 'type': 'int'},
                'GameNumber': {'aliases': ['game number', 'match number'], 'type': 'int'}
            },
            'aliases': ['game', 'games', 'match', 'matches']
        }
    }

    input_lower = user_input.lower().strip()
    input_tokens = set(input_lower.split())

    # Extract numeric values from input
    numbers = re.findall(r'\d+', input_lower)
    numbers = [int(num) for num in numbers] if numbers else []
    used_numbers = set()

    has_limit = any(token in input_tokens for token in command_patterns['limit'])
    is_desc = any(token in input_tokens for token in command_patterns['desc'])
    is_asc = any(token in input_tokens for token in command_patterns['asc'])
    is_group = any(token in input_tokens for token in command_patterns['group'])
    has_aggregate = any(input_tokens.intersection(patterns)
                        for command, patterns in command_patterns.items()
                        if command in ['count', 'average', 'maximum', 'minimum', 'sum'])

    order_direction = "DESC" if is_desc else "ASC" if is_asc else None

    query = {
        'select': [],
        'table': '',
        'join_table': '',
        'join_condition': '',
        'where': [],
        'group_by': [],
        'having': [],
        'order_by': [],
        'limit': None,
        'order_direction': order_direction
    }

    # Detect tables mentioned
    tables_mentioned = []
    for table, info in schemas.items():
        table_aliases = [table.lower()] + info['aliases']
        if input_tokens.intersection(table_aliases):
            tables_mentioned.append(table)

    columns_found = {}
    for table, schema in schemas.items():
        columns_found[table] = []
        for col, col_info in schema['columns'].items():
            aliases = col_info['aliases']
            col_aliases = [col.lower()] + aliases
            if input_tokens.intersection(col_aliases):
                columns_found[table].append(col)

    if not tables_mentioned:
        # No tables detected, use columns to guess
        tables_with_columns = [table for table, cols in columns_found.items() if cols]
        if len(tables_with_columns) == 1:
            query['table'] = tables_with_columns[0]
        elif len(tables_with_columns) > 1:
            query['table'] = max(columns_found.items(), key=lambda x: len(x[1]))[0]
        else:
            query['table'] = 'Players'
    else:
        query['table'] = tables_mentioned[0]

    table_schema = schemas[query['table']]

    # Handle JOIN
    if len(tables_mentioned) >= 2 and any(token in input_tokens for token in command_patterns['join']):
        primary_table = tables_mentioned[0]
        for secondary_table in tables_mentioned[1:]:
            if (primary_table, secondary_table) in table_relationships:
                join_cols = table_relationships[(primary_table, secondary_table)]
                query['join_table'] = secondary_table
                query['join_condition'] = f"{primary_table}.{join_cols[0]} = {secondary_table}.{join_cols[1]}"
                break
            elif (secondary_table, primary_table) in table_relationships:
                join_cols = table_relationships[(secondary_table, primary_table)]
                query['join_table'] = secondary_table
                query['join_condition'] = f"{secondary_table}.{join_cols[0]} = {primary_table}.{join_cols[1]}"
                break
        else:
            return False, "These tables cannot be joined directly."

    selected_columns = columns_found.get(query['table'], [])
    aggregate_columns = []
    group_columns = []
    order_columns = []

    for col in selected_columns:
        aggregates = detect_aggregates(input_lower, col, command_patterns)
        if aggregates:
            aggregate_columns.extend(aggregates)
        if is_group and any(alias in input_lower for alias in table_schema['columns'][col]['aliases'] + [col.lower()]):
            group_columns.append(col)
        if any(token in input_tokens for token in command_patterns['order']) and \
                any(alias in input_lower for alias in table_schema['columns'][col]['aliases'] + [col.lower()]):
            order_columns.append(col)

    top_n_value, order_column_phrase = extract_top_n_phrase(input_lower)
    if top_n_value:
        query['limit'] = top_n_value
        used_numbers.add(top_n_value)
        query['order_direction'] = 'DESC'  # top implies descending

        found_column = False
        if order_column_phrase:
            column_phrase_cleaned = ' '.join([w for w in order_column_phrase.split() if w not in ['and', 'with']])
            for col, col_info in table_schema['columns'].items():
                if column_phrase_cleaned in ([col.lower()] + col_info['aliases']):
                    query['order_by'].append(col)
                    found_column = True
                    break
        else:
            # No specific column, just pick the first selected column or a default
            if selected_columns:
                query['order_by'].append(selected_columns[0])
                found_column = True
            else:
                query['order_by'].append('AssistsPerGame')
                found_column = True

        if found_column and query['order_by'][0] not in selected_columns:
            selected_columns.append(query['order_by'][0])

    # Remove numbers used in top N
    numbers = [num for num in numbers if num not in used_numbers]

    conditions = parse_conditions(input_lower, table_schema, comparison_patterns, comparison_patterns_map,
                                  aggregate_columns, used_numbers)
    if conditions['where']:
        query['where'].extend(conditions['where'])
    if conditions['having']:
        query['having'].extend(conditions['having'])

    # Build SELECT clause
    if is_group:
        if group_columns:
            query['group_by'].extend(group_columns)
            query['select'].extend(group_columns)
            if aggregate_columns:
                query['select'].extend(aggregate_columns)
        else:
            return False, "Please specify the columns to group by."
    else:
        if aggregate_columns:
            query['select'].extend(aggregate_columns)
        elif selected_columns:
            # If user said "choose name" and we found multiple columns,
            # pick them. If none, default to '*'
            query['select'].extend(selected_columns)
        else:
            query['select'].append('*')

    # Handle ordering
    if query['order_by']:
        if not query['order_direction']:
            query['order_direction'] = 'ASC'
        query['order_by'] = [f"{col} {query['order_direction']}" for col in query['order_by']]

    # Apply LIMIT from remaining numbers if needed
    if has_limit and numbers and not query['limit']:
        query['limit'] = numbers[-1]

    # Construct final query
    select_clause = ', '.join(query['select']) if query['select'] else '*'
    sql_parts = [f"SELECT {select_clause}", f"FROM {query['table']}"]

    if query['join_table']:
        sql_parts.append(f"JOIN {query['join_table']} ON {query['join_condition']}")

    if query['where']:
        sql_parts.append(f"WHERE {' AND '.join(query['where'])}")
    if query['group_by']:
        sql_parts.append(f"GROUP BY {', '.join(query['group_by'])}")
    if query['having']:
        sql_parts.append(f"HAVING {' AND '.join(query['having'])}")
    if query['order_by']:
        sql_parts.append(f"ORDER BY {', '.join(query['order_by'])}")
    if query['limit']:
        sql_parts.append(f"LIMIT {query['limit']}")

    final_query = ' '.join(sql_parts)
    return True, final_query


def prompt_natural():
    """Interactive prompt for natural language queries."""
    while True:
        print("\nEnter natural language query (or 'exit' to quit):")
        user_input = input()

        if user_input.lower() == 'exit':
            break

        try:
            success, result = natural_language_to_sql(user_input)
            if success:
                while True:
                    print("\nSuggested SQL Query:")
                    print(result)
                    execute_input = input('Execute this query to the database? Y/N\n')
                    if execute_input.lower() == 'y':
                        print(connect.chatDB().execute_query(result))
                        break
                    elif execute_input.lower() == 'n':
                        break
                    elif execute_input.lower() == 'exit':
                        return
                    else:
                        # Treat any other input as a new query
                        user_input = execute_input.strip()
                        if user_input:
                            success, result = natural_language_to_sql(user_input)
                            if success:
                                continue
                            else:
                                print(f"\n{result}")
                                break
                        else:
                            print("Invalid input. Please enter 'Y' or 'N', or a new query.")
            else:
                print(f"\n{result}")
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try rephrasing your query.")


def main():
    """Main function."""
    prompt_natural()


if __name__ == "__main__":
    main()
