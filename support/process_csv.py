# define process_csv function
def process_csv(temp_folder_path: str, file_path: str) -> dict[bool, str]: #type: ignore
    # importing python module:S01
    try:
        from pathlib import Path
        import pandas as pd
    except Exception as error:
        print(f'ERROR - [Process-CSV:S01] - {str(error)}')

    # check if "temp" folder is present:S02
    try:
        # convert "temp" folder string into Path object
        temp_folder_path_object = Path(temp_folder_path) #type: ignore
        if (not ((temp_folder_path_object.exists()) and (temp_folder_path_object.is_dir()))):
            return {False: '"temp" Folder Is Not Present'}
    except Exception as error:
        print(f'ERROR - [Process-CSV:S02] - {str(error)}')

    # check if "file_path" file is present and has ".csv" extension:S03
    try:
        # convert "file_path" string into Path object
        file_path_object = Path(file_path)
        if (not ((file_path_object.exists()) and (file_path_object.is_file()) and (file_path_object.suffix.lower() == '.csv'))):
            return {False: f'"{file_path_object.name}" Is Not A Valid File Type'}
    except Exception as error:
        print(f'ERROR - [Process-CSV:S03] - {str(error)}')

    # modify the ".csv" file column header:S04
    try:
        # read the ".csv" file
        file_data_frame = pd.read_csv(file_path_object, low_memory = False)
        # modify the changes
        file_data_frame.columns = [col.lower().replace(' ', '_') for col in file_data_frame.columns]
    except Exception as error:
        print(f'ERROR - [Process-CSV:S04] - {str(error)}')

    # save new ".csv" file:S05
    try:
        # define ".csv" file path
        output_file_path = temp_folder_path_object / file_path_object.name #type: ignore
        # save the modifed file
        file_data_frame.to_csv(output_file_path, index = False)
    except Exception as error:
        print(f'ERROR - [Process-CSV:S05] - {str(error)}')