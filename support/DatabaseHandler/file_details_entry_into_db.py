# define file_details_entry_into_db function
def file_details_entry_into_db(env_file_path: str, input_file_path: str) -> dict[str, str]: #type: ignore
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

    # load ".env" file":S03
    try:
        load_dotenv(dotenv_path = env_file_path_object)
    except Exception as error:
        return {'status' : 'ERROR', 'message': f'[File-Details-Entry-Into-DB:S03] - {str(error)}'}

    # check if "input_file_path" is present or not:S04
    try:
        # converting "input_file_path" string into Path object
        input_file_path_object = Path(input_file_path)
        if (not (input_file_path_object.exists()) and (input_file_path_object.is_file())):
            return {'status': 'ERROR', 'message': f'"{input_file_path_object.name}" File Is Not Appropiate To Use'}
    except Exception as error:
        return {'status' : 'ERROR', 'message': f'[File-Details-Entry-Into-DB:S04] - {str(error)}'}

    # fetching file extension and check allowed list:S05
    try:
        # define allowed extension
        allowed_extension = ['csv', 'xls', 'xlsx']
        input_file_extension = input_file_path_object.suffix.lstrip('.')
        # check if file extension not match with allowed one
        if (not (input_file_extension in allowed_extension)):
            return {'status' : 'ERROR', 'message': f'"{input_file_path_object.name}" File Is Not Matched With Allowed File Type'}
    except Exception as error:
        return {'status' : 'ERROR', 'message': f'[File-Details-Entry-Into-DB:S05] - {str(error)}'}

    # fetching file size:S06
    try:
        input_file_size = input_file_path_object.stat().st_size
        # check if file size not 0-bytes
        if (not (input_file_size > 0)):
            return {'status' : 'ERROR', 'message': f'"{input_file_path_object.name}" File Is Empty'}
    except Exception as error:
        return {'status' : 'ERROR', 'message': f'[File-Details-Entry-Into-DB:S06] - {str(error)}'}

    return {'status' : 'SUCCESS', 'message' : f'Extension: {input_file_extension}; Size: {input_file_size}'}