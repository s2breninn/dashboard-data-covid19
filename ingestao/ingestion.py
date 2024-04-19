import os
import sys
import glob
import shutil

sys.path.insert(0, os.getcwd())
from utils.get_element_selenium import get_element_data

def mov_file():
    root_folder = os.getcwd()
    data_folder = os.path.join(os.path.join(root_folder, 'data'))
    user_folder = os.path.expanduser('~')
    downloads_dir = os.path.join(user_folder, 'Downloads')

    search_pattern = os.path.join(downloads_dir, "HIST_PAINEL_COVIDBR_12abr2024.zip")
    matching_files = glob.glob(search_pattern)

    if matching_files:
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        shutil.move(matching_files[0], data_folder)

    else:
        print("Arquivo não encontrado na pasta de Downloads.")


if __name__ == '__main__':
    url = 'https://covid.saude.gov.br/'
    elemento = '/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-content/div[1]/div[2]/ion-button'

    get_element_data(url, xpath=elemento)
    mov_file()