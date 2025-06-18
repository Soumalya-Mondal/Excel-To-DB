# define file_details_entry_into_db function
def file_details_entry_into_db(env_file_path: str, input_file_path: str, account_name: str) -> dict[str, str]: #type: ignore
    # importing python module:S01
    try:
        from pathlib import Path
        from dotenv import load_dotenv
        import os
        import random
        import string
        from datetime import datetime, timezone
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

    # define database connection parameter:S07
    try:
        database_connection_parameter = {
            "dbname": os.getenv('DATABASE_NAME'),
            "user": os.getenv('DATABASE_USER'),
            "password": os.getenv('DATABASE_PASSWORD'),
            "host": os.getenv('DATABASE_HOST'),
            "port": os.getenv('DATABASE_PORT')
        }
    except Exception as error:
        return {'status' : 'ERROR', 'message': f'[File-Details-Entry-Into-DB:S07] - {str(error)}'}

    # checking if "table_name_for_file_data" not present inside database:S08
    try:
        while True:
            # define sql for "table_name_for_file_data" present inside database
            check_table_name_for_file_data_sql = '''
            SELECT EXISTS (
                SELECT 1 FROM account_file_list
                WHERE table_name_for_file_data = %s);'''

            # generating "unique_table_name_for_title_data":S08-A
            try:
                unique_table_name_for_title_data = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
            except Exception as error:
                return {'status' : 'ERROR', 'message': f'[File-Details-Entry-Into-DB:S08-A] - {str(error)}'}

            # execute the query for checking:S08-B
            try:
                with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                    with database_connection.cursor() as database_cursor:
                        database_cursor.execute(check_table_name_for_file_data_sql, (unique_table_name_for_title_data,))
                        unique_table_already_present_status = database_cursor.fetchone()[0]
                        if not unique_table_already_present_status:
                            break
            except Exception as error:
                return {'status' : 'ERROR', 'message': f'[File-Details-Entry-Into-DB:S08-B] - {str(error)}'}
    except Exception as error:
        return {'status' : 'ERROR', 'message': f'[File-Details-Entry-Into-DB:S08] - {str(error)}'}

    # inserting file details into database:S09
    try:
        # define sql to insert file details
        file_details_insert_sql = '''
            INSERT INTO account_file_list (
                account_name,
                file_submitted_date,
                submitted_file_name,
                file_path,
                file_size_in_byte,
                file_process_status,
                table_name_for_file_data,
                file_type
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'''

        # creating file details data for insert:S09-A
        try:
            file_details_to_insert = (
                account_name,                               # account_name
                datetime.now(timezone.utc),                 # file_submitted_date
                str(input_file_path_object.name),           # submitted_file_name
                str(input_file_path),                       # file_path
                input_file_size,                            # file_size_in_byte
                0,                                          # file_process_status
                unique_table_name_for_title_data,           # table_name_for_file_data
                input_file_path_object.suffix.lstrip('.')   # file_type
            )
        except Exception as error:
            return {'status' : 'ERROR', 'message': f'[File-Details-Entry-Into-DB:S09-A] - {str(error)}'}

        # execute file details insert query:S09-B
        try:
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(file_details_insert_sql, file_details_to_insert)
                    database_connection.commit()
        except Exception as error:
            return {'status' : 'ERROR', 'message': f'[File-Details-Entry-Into-DB:S09-B] - {str(error)}'}
    except Exception as error:
        return {'status' : 'ERROR', 'message': f'[File-Details-Entry-Into-DB:S09] - {str(error)}'}

    # check if data successfully inserted or not:S12
    try:
        # define sql for check if data inserted
        file_details_insert_check_sql = '''
        SELECT * FROM account_file_list
        WHERE table_name_for_file_data = %s;'''

        # execute file details check query:S12-A
        try:
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(file_details_insert_check_sql, (unique_table_name_for_title_data,))
                    file_details_insert_result = database_cursor.fetchone()
                    # check the result
                    if file_details_insert_result:
                        return {'status' : 'SUCCESS', 'message' : f'"{input_file_path_object.name}" File Submitted With "{unique_table_name_for_title_data}" Unique Table Name'}
                    else:
                        return {'status' : 'SUCCESS', 'message' : f'"{input_file_path_object.name}" File Not Submitted'}
        except Exception as error:
            return {'status' : 'ERROR', 'message': f'[File-Details-Entry-Into-DB:S12-A] - {str(error)}'}
    except Exception as error:
        return {'status' : 'ERROR', 'message': f'[File-Details-Entry-Into-DB:S12] - {str(error)}'}