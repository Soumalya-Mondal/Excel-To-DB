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
        input_folder_path = Path(parent_folder_path) / 'input'
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

    # check if ".env" file is present:S05
    try:
        if (not (env_file_path.exists())):
            print('ERROR - ".env" Not Present, Hence Stop Execution')
            sys.exit(1)
    except Exception as error:
        print(f'ERROR - [Excel-To-DB:S05] - {str(error)}')

    # fetching all the "excel" or "csv" file from the directory:S06
    try:
        # define file extension
        allowed_file_extension = ['.csv', 'xls', '.xlsx']
        # find all the files with the spcified extension
        found_file_list = [str(file_path.resolve()) for file_path in input_folder_path.iterdir() if file_path.suffix.lower() in allowed_file_extension]
        # check if any files are present
        if (len(found_file_list) > 0):
            # print all the files name
            for file_path in found_file_list:
                print(f'INFO    - "{Path(file_path).name}" File Found')
        else:
            print('ERROR   - No Files Present Inside "input" Folder, Hence Stop Execution')
            sys.exit(1)
    except Exception as error:
        print(f'ERROR - [Excel-To-DB:S06] - {str(error)}')

    # importing "process_csv" user-define function:S07
    try:
        from support.process_csv import process_csv
    except Exception as error:
        print(f'ERROR - [Excel-To-DB:S07] - {str(error)}')

    # loop through all the files:S08
    try:
        for file_path in found_file_list:
            # calling "process_csv" function
            process_csv(temp_folder_path = str(temp_folder_path), file_path = str(file_path))
    except Exception as error:
        print(f'ERROR - [Excel-To-DB:S08] - {str(error)}')