# define main function
if __name__ == '__main__':
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        from dotenv import load_dotenv
    except Exception as error:
        print(f'ERROR - [Excel-To-DB:S01] - {str(error)}')

    # define folder and file path:S02
    try:
        parent_folder_path = Path.cwd()
        input_folder_path = Path(parent_folder_path) / 'input'
        env_file_path = Path(parent_folder_path) / '.env'
    except Exception as error:
        print(f'ERROR - [Excel-To-DB:S02] - {str(error)}')

    # check if "input" folder is present:S03
    try:
        if ((input_folder_path.exists()) and (input_folder_path.is_dir())):
            print('INFO    - "input" Folder Already Present\n')
        else:
            # creating "input" folder
            input_folder_path.mkdir()
            # check if "input" folder created or not
            if ((input_folder_path.exists()) and (input_folder_path.is_dir())):
                print('SUCCESS - "input" Folder Created\n')
            else:
                print('ERROR   - "input" Folder Not Created, Hence Stop Execution')
                sys.exit(1)
    except Exception as error:
        print(f'ERROR - [Excel-To-DB:S0#] - {str(error)}')

    # check if ".env" file is present:S04
    try:
        if (not (env_file_path.exists())):
            print('ERROR - ".env" Not Present, Hence Stop Execution')
            sys.exit(1)
    except Exception as error:
        print(f'ERROR - [Excel-To-DB:S04] - {str(error)}')

    # fetching all the "excel" or "csv" file from the directory:S05
    try:
        # define file extension
        allowed_file_extension = ['.csv', 'xls', '.xlsx']
        # find all the files with the spcified extension
        found_file_list = [str(file.resolve()) for file in input_folder_path.iterdir() if file.suffix.lower() in allowed_file_extension]
        # check if any files are present
        if (len(found_file_list) > 0):
            # print all the files name
            for file in found_file_list:
                print(f'INFO    - "{Path(file).name}" File Found')
        else:
            print('ERROR   - No Files Present Inside "input" Folder, Hence Stop Execution')
            sys.exit(1)
    except Exception as error:
        print(f'ERROR - [Excel-To-DB:S05] - {str(error)}')

    # load ".env" file:S06
    try:
        load_dotenv(dotenv_path = env_file_path)
    except Exception as error:
        print(f'ERROR - [Excel-To-DB:S06] - {str(error)}')