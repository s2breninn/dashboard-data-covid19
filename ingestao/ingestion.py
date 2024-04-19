import os
import sys
import glob
import shutil

sys.path.insert(0, os.getcwd())
from utils.get_element_selenium import get_element_data
from utils.extract_file import extract_file

def move_file(downloads_dir, folder_files_zip):
    search_pattern = os.path.join(downloads_dir, "HIST_PAINEL_COVIDBR_13abr2024.zip")
    matching_files = glob.glob(search_pattern)

    if matching_files:
        if not os.path.exists(folder_files_zip):
            os.makedirs(folder_files_zip)

        shutil.move(matching_files[0], folder_files_zip)

    else:
        print("Arquivo não encontrado na pasta de Downloads.")


if __name__ == '__main__':
    root_folder = os.getcwd()
    data_folder = os.path.join(os.path.join(root_folder, 'data'))
    user_folder = os.path.expanduser('~')
    downloads_dir = os.path.join(user_folder, 'Downloads')

    folder_files_zip = os.path.join(data_folder, 'zip_files')
    folder_extracted_files = os.path.join(data_folder, 'extracted_files')

    url = 'https://covid.saude.gov.br/'
    elemento = '/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-content/div[1]/div[2]/ion-button'

    get_element_data(url, xpath=elemento)
    move_file(downloads_dir, folder_files_zip)
    extract_file(folder_extracted_files, folder_files_zip)