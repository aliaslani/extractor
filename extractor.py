import zipfile
import py7zr
import rarfile
import os

def extract_zip(file_path, extract_to, password=None):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        if password:
            zip_ref.setpassword(password.encode())
        zip_ref.extractall(extract_to)

def extract_7z(file_path, extract_to, password=None):
    with py7zr.SevenZipFile(file_path, mode='r', password=password) as archive:
        archive.extractall(path=extract_to)

def extract_rar(file_path, extract_to, password=None):
    with rarfile.RarFile(file_path) as rar_ref:
        if password:
            rar_ref.setpassword(password)
        rar_ref.extractall(extract_to)

def extract_file(file_path, extract_to, password=None):
    if file_path.endswith('.zip'):
        extract_zip(file_path, extract_to, password)
    elif file_path.endswith('.7z'):
        extract_7z(file_path, extract_to, password)
    elif file_path.endswith('.rar'):
        extract_rar(file_path, extract_to, password)
    else:
        print(f"Unsupported file format: {file_path}")

def extract_recursive(file_path, extract_to, password=None):
    extract_file(file_path, extract_to, password)
    # Check for compressed files within the extracted content and extract them too
    for root, dirs, files in os.walk(extract_to):
        for file in files:
            full_path = os.path.join(root, file)
            if full_path.endswith(('.zip', '.7z', '.rar')):
                new_extract_to = os.path.join(root, os.path.splitext(file)[0])
                os.makedirs(new_extract_to, exist_ok=True)
                extract_file(full_path, new_extract_to, password)

# Example usage
extract_to_directory = 'path/to/extract'
compressed_file_path = 'path/to/compressed/file.zip'
password = 'your_password'

extract_recursive(compressed_file_path, extract_to_directory, password)
