# define file_name_entry_into_db function
def file_name_entry_into_db(env_file_path: str, input_file_path: str) -> dict[str, str]: #type: ignore
    # importing python module:S01
    try:
        from pathlib import Path
        from dotenv import load_dotenv
        import os
        import psycopg2
    except Exception as error:
        return {'status' : 'ERROR', 'message': f'[File-Details-Entry-Into-DB:S01] - {str(error)}'}

    # check if ".env" file is present:S02
    try:
        # converting ".env" file string to Path object
        env_file_path_object = Path(env_file_path)
        if (not ((env_file_path_object.exists()) and (env_file_path_object.is_file()))):
            return {'status': 'ERROR', 'message': '".env" File Is Not Appropiate To Use'}
    except Exception as error:
        return {'status' : 'ERROR', 'message': f'[File-Details-Entry-Into-DB:S02] - {str(error)}'}

    # load ".env" file"S03
    try:
        load_dotenv(dotenv_path = env_file_path_object)
    except Exception as error:
        return {'status' : 'ERROR', 'message': f'[File-Details-Entry-Into-DB:S03] - {str(error)}'}