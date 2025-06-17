# define main function
if __name__ == '__main__':
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
    except Exception as error:
        print(f'ERROR - [Excel-To-DB:S01] - {str(error)}')

    # define folder and file path:S02
    try:
        parent_folder_path = Path.cwd()
        resource_folder_path = Path(parent_folder_path) / 'resource'
        input_folder_path = Path(resource_folder_path) / 'input'
        env_file_path = Path(parent_folder_path) / '.env'
        temp_folder_path = Path(parent_folder_path) / 'temp'
    except Exception as error:
        print(f'ERROR - [Excel-To-DB:S02] - {str(error)}')

    # append system path:S03
    try:
        sys.path.append(str(parent_folder_path))
    except Exception as error:
        print(f'ERROR - [Excel-To-DB:S03] - {str(error)}')

    # check if "input" folder is present:S04
    try:
        if ((input_folder_path.exists()) and (input_folder_path.is_dir())):
            print('INFO    - "input" Folder Already Present')
        else:
            # creating "input" folder
            input_folder_path.mkdir()
            # check if "input" folder created or not
            if ((input_folder_path.exists()) and (input_folder_path.is_dir())):
                print('SUCCESS - "input" Folder Created')
            else:
                print('ERROR   - "input" Folder Not Created, Hence Stop Execution')
                sys.exit(1)
    except Exception as error:
        print(f'ERROR - [Excel-To-DB:S04] - {str(error)}')

    # check if "temp" folder is present:S05
    try:
        if ((temp_folder_path.exists()) and (temp_folder_path.is_dir())):
            print('INFO    - "temp" Folder Already Present\n')
        else:
            # creating "temp" folder
            temp_folder_path.mkdir()
            # check if "temp" folder created or not
            if ((temp_folder_path.exists()) and (temp_folder_path.is_dir())):
                print('SUCCESS - "temp" Folder Created\n')
            else:
                print('ERROR   - "temp" Folder Not Created, Hence Stop Execution')
                sys.exit(1)
    except Exception as error:
        print(f'ERROR - [Excel-To-DB:S05] - {str(error)}')

    # check if ".env" file is present:S06
    try:
        if (not (env_file_path.exists())):
            print('ERROR - ".env" Not Present, Hence Stop Execution')
            sys.exit(1)
    except Exception as error:
        print(f'ERROR - [Excel-To-DB:S06] - {str(error)}')

    # creating "account_file_list" table inside database:S07
    try:
        # define "account_file_list" table create sql query
        account_file_list_table_create_sql = '''
        CREATE TABLE account_file_list (
            id SERIAL PRIMARY KEY,
            account_name VARCHAR(255) NOT NULL,
            file_submitted_date TIMESTAMP WITH TIME ZONE NOT NULL,
            submitted_file_name VARCHAR(255) NOT NULL,
            file_path TEXT NOT NULL,
            file_size_in_byte BIGINT NOT NULL,
            file_process_status INT NOT NULL CHECK (file_process_status IN (0, 1, 2, 3, 4, 5, 6)),
            table_name_for_file_data CHAR(16) NOT NULL CHECK (char_length(table_name_for_file_data) = 16),
            file_type VARCHAR(4) NOT NULL CHECK (LOWER(file_type) IN ('csv', 'xls', 'xlsx'))
        );
        ALTER TABLE account_file_list OWNER TO soumalya;'''

        # importing "database_table_create" function:S07-A
        try:
            from support.DatabaseHandler.database_table_create import database_table_create
        except Exception as error:
            print(f'ERROR - [Excel-To-DB:S07-A] - {str(error)}')

        # calling "database_table_create" user define function:S07-B
        try:
            account_file_list_function_response = database_table_create(env_file_path = str(env_file_path), table_name = 'account_file_list', table_create_sql = str(account_file_list_table_create_sql))
            # check the response
            if (account_file_list_function_response == None):
                print(f'ERROR   - "database_table_create" Function Not Executed Proerly, Manual Intervention Is Required')
                sys.exit(1)
            else:
                if (str(account_file_list_function_response['status']).lower() == 'success'):
                    print(f"SUCCESS - {account_file_list_function_response['message']}")
                else:
                    print(f"{str(account_file_list_function_response['status']).upper()} - {account_file_list_function_response['message']}, Hence Stop Execution")
                    sys.exit(1)
        except Exception as error:
            print(f'ERROR - [Excel-To-DB:S07-B] - {str(error)}')
    except Exception as error:
        print(f'ERROR - [Excel-To-DB:S07] - {str(error)}')

    # # fetching all the "excel" or "csv" file from the directory:S09
    # try:
    #     # define file extension
    #     allowed_file_extension = ['.csv', 'xls', '.xlsx']
    #     # find all the files with the spcified extension
    #     found_file_list = [str(file_path.resolve()) for file_path in input_folder_path.iterdir() if file_path.suffix.lower() in allowed_file_extension]
    #     # check if any files are present
    #     if (len(found_file_list) > 0):
    #         # print all the files name
    #         for file_path in found_file_list:
    #             print(f'INFO    - "{Path(file_path).name}" File Found')
    #     else:
    #         print('ERROR   - No Files Present Inside "input" Folder, Hence Stop Execution')
    #         sys.exit(1)
    # except Exception as error:
    #     print(f'ERROR - [Excel-To-DB:S09] - {str(error)}')

    # # importing "process_csv" user-define function:S10
    # try:
    #     from support.process_csv import process_csv
    # except Exception as error:
    #     print(f'ERROR - [Excel-To-DB:S10] - {str(error)}')

    # # loop through all the files:S11
    # try:
    #     for file_path in found_file_list:
    #         # calling "process_csv" function
    #         process_csv(temp_folder_path = str(temp_folder_path), file_path = str(file_path))
    # except Exception as error:
    #     print(f'ERROR - [Excel-To-DB:S11] - {str(error)}')