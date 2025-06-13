# define database_table_create function
def database_table_create(env_file_path: str, table_name: str, table_create_sql: str)  -> dict[str, str]: #type: ignore
    # importing python module:S01
    try:
        from pathlib import Path
        from dotenv import load_dotenv
        import os
        import psycopg2
    except Exception as error:
        print(f'ERROR - [Database-Table-Create:S01] - {str(error)}')

    # check if ".env" file is present:S02
    try:
        # converting ".env" file string to Path object
        env_file_path_object = Path(env_file_path)
        if (not ((env_file_path_object.exists()) and (env_file_path_object.is_file()))):
            return {'status': 'SUCCESS', 'message': '".env" File Is Not Appropiate To Use'}
    except Exception as error:
        print(f'ERROR - [Database-Table-Create:S02] - {str(error)}')

    # load ".env" file"S03
    try:
        load_dotenv(dotenv_path = env_file_path_object)
    except Exception as error:
        print(f'ERROR - [Database-Table-Create:S03] - {str(error)}')

    # define database connection parameter:S04
    try:
        database_connection_parameter = {
            "dbname": os.getenv('DATABASE_NAME'),
            "user": os.getenv('DATABASE_USER'),
            "password": os.getenv('DATABASE_PASSWORD'),
            "host": os.getenv('DATABASE_HOST'),
            "port": os.getenv('DATABASE_PORT')
        }
    except Exception as error:
        print(f'ERROR - [Database-Table-Create:S04] - {str(error)}')

    # define "table_name" table create check sql query:S05
    try:
        table_create_check_sql = f'''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = '{table_name}'
        );'''
    except Exception as error:
        print(f'ERROR - [Database-Table-Create:S05] - {str(error)}')

    # check if "table_name" table is already present:S06
    try:
        with psycopg2.connect(**database_connection_parameter) as database_connection:  # type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(table_create_check_sql)
                table_already_present_result = database_cursor.fetchone()[0]
                if table_already_present_result:
                    return {'status': 'SUCCESS', 'message': f'"{table_name}" Already Present Inside Database'}
    except Exception as error:
        print(f'ERROR - [Database-Table-Create:S06] - {str(error)}')

    # connect database and execute table create query:S07
    try:
        with psycopg2.connect(**database_connection_parameter) as database_connection: # type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(table_create_sql)
    except Exception as error:
        print(f'ERROR - [Database-Table-Create:S07] - {str(error)}')

    # check if "account_file_list" table is created:S08
    try:
        with psycopg2.connect(**database_connection_parameter) as database_connection:  # type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(table_create_check_sql)
                account_file_list_table_created_result = database_cursor.fetchone()[0]
                if account_file_list_table_created_result:
                    return {'status': 'SUCCESS', 'message': f'"{table_name}" Created Successfully Inside Database'}
                else:
                    return {'status': 'ERROR', 'message': f'"{table_name}" Not Created Inside Database'}
    except Exception as error:
        print(f'ERROR - [Database-Table-Create:S08] - {str(error)}')