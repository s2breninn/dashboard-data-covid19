import os
import zipfile

def get_expected_files_from_zip(path_file_zip):
    expected_files = []
    with zipfile.ZipFile(path_file_zip, 'r') as zip_ref:
        expected_files = zip_ref.namelist()

    return expected_files

def check_extracted_files(folder_extracted_files, expected_files):
    extract_files = set(os.listdir(folder_extracted_files))

    expected_files_set = set(expected_files)

    if expected_files_set.issubset(extract_files):
        return True
    else:
        return False

def extract_file(folder_extracted_files, folder_files_zip):
    if not os.path.exists(folder_extracted_files):
        os.makedirs(folder_extracted_files)

    for file in os.listdir(folder_files_zip):
        if file.endswith('.zip'):
            path_file_zip = os.path.join(folder_files_zip, file)

            expected_files = get_expected_files_from_zip(path_file_zip)
            check_value = check_extracted_files(folder_extracted_files, expected_files)

            if check_value == False:
                with zipfile.ZipFile(path_file_zip, 'r') as zip_ref:
                    zip_ref.extractall(folder_extracted_files)
            else: 
                print(f'Arquivos já extraidos')