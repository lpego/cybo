### This script puts all the files with sensitive
### information in a zip archive

import os
import zipfile
import pyminizip
import getpass
import datetime

def create_zip_archive(output_filename, folders, files, password):
    temp_zip = 'cybo_private_files.zip'
    with zipfile.ZipFile(temp_zip, 'w') as zipf:
        for folder in folders:
            for root, _, filenames in os.walk(folder):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    zipf.write(file_path, os.path.relpath(file_path, os.path.join(folder, '..')))
        
        for file in files:
            zipf.write(file, os.path.basename(file))
    
    pyminizip.compress(temp_zip, None, output_filename, password, 5)
    os.remove(temp_zip)

if __name__ == "__main__":
    time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    root = 'D:/cybo'
    folders_to_zip = ['certificates', 'graphics', 'webinars', 'website_exports']
    files_to_zip = [f'{root}/scripts/client_secret.json', f'{root}/webinars_cybo2024_v4.1_compressed.pdf']
    output_zip = f'{root}/cybo_archive_{time}.zip'
    
    password = getpass.getpass('Enter password for the ZIP archive: ')

    create_zip_archive(output_zip, folders_to_zip, files_to_zip, password)
    print(f'Created {output_zip} successfully.')