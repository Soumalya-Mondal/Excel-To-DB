# define file_path_fetch_for_process function
def file_path_fetch_for_process(env_file_path: str) -> dict[str, str | list]: #type: ignore
    # importing python module:S01
    try:
        from pathlib import Path
        from dotenv import load_dotenv
        import os
        import psycopg2
    except Exception as error:
        return {'status' : 'ERROR', 'message': f'[File-Path-Fetch-For-Process:S01] - {str(error)}', 'file_path_list' : []}

    # check if ".env" file is present:S02
    try:
        # converting ".env" file string to Path object
        env_file_path_object = Path(env_file_path)
        if (not ((env_file_path_object.exists()) and (env_file_path_object.is_file()))):
            return {'status': 'ERROR', 'message': '".env" File Is Not Appropiate To Use'}
    except Exception as error:
        return {'status' : 'ERROR', 'message': f'[File-Path-Fetch-For-Process:S02] - {str(error)}'}

    # load ".env" file"S03
    try:
        load_dotenv(dotenv_path = env_file_path_object)
    except Exception as error:
        return {'status' : 'ERROR', 'message': f'[File-Path-Fetch-For-Process:S03] - {str(error)}'}

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
        return {'status' : 'ERROR', 'message': f'[File-Path-Fetch-For-Process:S04] - {str(error)}'}